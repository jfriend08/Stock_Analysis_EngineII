package ticker;

import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class TickerMapper extends Mapper<LongWritable, Text, Text, IntWritable>{
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		String line = value.toString();
		BufferedReader data = new BufferedReader(new InputStreamReader(new FileInputStream("companylist02.txt")));
		data.readLine();
		HashMap<String, String> hash01 =  new HashMap<>();
		String line02;
		while((line02 = data.readLine()) != null && line02 != "") {
			String[] holder = line02.split("	");
			String tag = holder[0];
			String sector = holder[5];
			String industry = holder[6];
			String classes = sector + ", " + industry;  // sector industry
			hash01.put(tag, classes);
		}
		data.close();
		
		String time, content;
		String[] holder = line.split("	");
		time = holder[0];
		
		///////
		try {
		content = holder[2];
		
		int multi = 0;
	    int year = Integer.valueOf(time.split("-")[0]);
		switch(year) {
			case 2015:
				multi = 10;
				break;
			case 2014:
				multi = 10;
				break;
			case 2013:
				multi = 8;
				break;
			case 2012:
				multi = 6;
				break;
			case 2011:
				multi = 5;
				break;
			case 2010:
				multi = 4;
				break;
			default:
				multi = 10;
				break;
		}
		
		Pattern pattern = Pattern.compile("(?<=ticker=\").*?(?=:)");
		Matcher matcher = pattern.matcher(content);
		ArrayList<String> tagHolder = new ArrayList<>();
		while (matcher.find()) {
			String tag = matcher.group().toString();
			if (hash01.containsKey(tag)) {
				tagHolder.add(tag);
			}
		}
		
		if (tagHolder.size() > 1) {
			int size = tagHolder.size();
			for (int i = 0; i < size - 1; i++) {
				for (int k = i + 1; k < size; k++) {
					context.write(new Text(tagHolder.get(i) + "	" + tagHolder.get(k)), new IntWritable(multi));
					context.write(new Text(tagHolder.get(k) + "	" + tagHolder.get(i)), new IntWritable(multi));
				}
			}
		}
		} catch(Exception e) {
			
		}
		
		
	}

}
