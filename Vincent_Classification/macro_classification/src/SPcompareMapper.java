import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;



public class SPcompareMapper extends Mapper<LongWritable, Text, Text, IntWritable> {
	public void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
		String[] line = value.toString().split("	");
		String tag = line[0];
		String spline = new BufferedReader(new InputStreamReader(new FileInputStream("S&P20140401to20150406.csv"))).readLine();
		String[] spholder = spline.split(",");

		
		for(int i = 0; i < spholder.length; i++) {
			Double valueStock = Double.valueOf(line[i + 1]);
			Double valueSP = Double.valueOf(spholder[i]);
			if (valueSP >= 0) {
				if (valueStock <= 0) {
					context.write(new Text(tag + " 3") , new IntWritable(1));
				} else if (valueStock > valueSP) {
					context.write(new Text(tag + " 1"), new IntWritable(1));
				} else {
					context.write(new Text(tag + " 2"), new IntWritable(1));
				}
			} else {
				if (valueStock >= 0) {
					context.write(new Text(tag + " 6"), new IntWritable(1));
				} else if (valueStock < valueSP) {
					context.write(new Text(tag + " 4"), new IntWritable(1));
				} else {
					context.write(new Text(tag + " 5"), new IntWritable(1));
				}
			}
		}
		
	}

}
