import java.io.IOException;
import java.util.ArrayList;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class StubReducer extends Reducer<Text, Text, Text, Text> {

  @Override
  public void reduce(Text key, Iterable<Text> values, Context context)
      throws IOException, InterruptedException {

    /*
     * TODO implement
     */
	  
	  int total = 0;
	  ArrayList<String> valueList=new ArrayList<String>();
	  for (Text value:values) {
		  valueList.add(value.toString());
	  }
	  for (int i=0; i<valueList.size()-1; i++) {
//		  get the +/- from A
		  String Avalue=valueList.get(i);
		  String Aname=valueList.get(i).split(":")[0];
		  int lengthA=Avalue.length();
		  char Asign=Avalue.charAt(lengthA-1);
	    for (int j=i+1; j<valueList.size(); j++) {
//	    	get the +/- from B
	    	String Bvalue=valueList.get(j);
	    	String Bname=valueList.get(j).split(":")[0];
	    	if (Aname.equals(Bname)) continue;
	    	
	    	int lengthB=Bvalue.length();
	    	char Bsign=Bvalue.charAt(lengthB-1);
	    	if ((Asign+"").equals(Bsign+"")) {
	    		context.write(new Text(Aname+"-"+Bname), new Text(key.toString()+":"+1));
	    		context.write(new Text(Bname+"-"+Aname), new Text(key.toString()+":"+1));
	    	} else {
	    		context.write(new Text(Aname+"-"+Bname), new Text(key.toString()+":"+0));
	    		context.write(new Text(Bname+"-"+Aname), new Text(key.toString()+":"+0));
			}
	    }
	  }
	  
  }
}