import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class MergeMapper extends Mapper<LongWritable, Text, Text, Text > {
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		String[] holder = value.toString().split(" ");
		//System.out.println(holder[0] + "  " + holder[1]);
		context.write(new Text(holder[0]), new Text(holder[1]));
		

	}
}