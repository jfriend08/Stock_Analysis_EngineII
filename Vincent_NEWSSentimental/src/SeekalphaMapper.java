import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;
import org.jsoup.Connection.Response;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

import edu.stanford.nlp.ling.CoreAnnotations;
import edu.stanford.nlp.neural.rnn.RNNCoreAnnotations;
import edu.stanford.nlp.pipeline.Annotation;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import edu.stanford.nlp.sentiment.SentimentCoreAnnotations;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.util.CoreMap;

public class SeekalphaMapper extends Mapper<LongWritable, Text, Text, IntWritable>{
	static StanfordCoreNLP pipeline;

    public static void init() {
        pipeline = new StanfordCoreNLP("MyPropFile.properties");
    }

    public static int findSentiment(String tweet) {

        int mainSentiment = 0;
        if (tweet != null && tweet.length() > 0) {
            int longest = 0;
            Annotation annotation = pipeline.process(tweet);
            for (CoreMap sentence : annotation
                    .get(CoreAnnotations.SentencesAnnotation.class)) {
                Tree tree = sentence
                        .get(SentimentCoreAnnotations.AnnotatedTree.class);
                int sentiment = RNNCoreAnnotations.getPredictedClass(tree);
                String partText = sentence.toString();
                if (partText.length() > longest) {
                    mainSentiment = sentiment;
                    longest = partText.length();
                }

            }
        }
        return mainSentiment;
    }
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		String line = value.toString();
		String tag = line.split("	")[0];

		try {
			Response response= Jsoup.connect("http://seekingalpha.com/symbol/" + tag)
			           .ignoreContentType(true)
			           .userAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0")  
			           .referrer("http://www.google.com")   
			           .timeout(12000) 
			           .followRedirects(true)
			           .execute();
			Document doc = response.parse();
		    Elements anchors = doc.select("a");
		    ArrayList<String> holder = new ArrayList<>();
		    for (Element anchor : anchors) {
			    String link = anchor.attr("href");
			    if (link.length() >11 && link.substring(1, 9).equals("article/")) {
				    link = "http://seekingalpha.com" + link;
				    String[] templink = link.split("_");
				    if (templink[templink.length - 1].equals("header")) {
				    	continue;
				    } else {
				        holder.add(link);
				    }
			    }
		    }
		   
		    for (String ref : holder) {
		    	try {
		    	//System.out.println(ref);	    	
		        Response response2= Jsoup.connect(ref)
				           .ignoreContentType(true)
				           .userAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0")  
				           .referrer("http://www.google.com")   
				           .timeout(12000) 
				           .followRedirects(true)
				           .execute();
				Document remark = response2.parse();
		        Elements p = remark.select("p");
			    for(Element smallp : p) {
			    String comments = smallp.text();
			    init();
			    context.write(new Text(tag), new IntWritable(findSentiment(comments)));			
				}
			    
			    String[] idtagholder = ref.split("/|-");
			    String idtag = idtagholder[4];
			    
			    
			    	String url = "http://seekingalpha.com/memcached2/comment_group/article:" + idtag + ":more:" + 1;
			    	Response response3= Jsoup.connect(url)
					           .ignoreContentType(true)
					           .userAgent("Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:25.0) Gecko/20100101 Firefox/25.0")  
					           .referrer("http://www.google.com")   
					           .timeout(12000) 
					           .followRedirects(true)
					           .execute();
			    	
			    	remark = response3.parse();
			        p = remark.select("span[class=cont_com]");
				    for(Element smallp : p) {
				        String comments = smallp.text();
				        init();
				        context.write(new Text(tag), new IntWritable(findSentiment(comments)));
				    }
		    	}
			
		    	
			    
			    
		    	
		      catch (Exception ex){}
		    	
			}    
		} catch (Exception ex) {
		}
		
		
	}
}