import java.io.IOException;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;


public class Mapper2 extends Mapper<LongWritable, Text, Text, Text> {

	@Override
	public void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {

		/*
		 * TODO implement
		 */

		// read each line
		// name Index Open High Low Close Volume AdjClose
		String line = value.toString();
		String[] details = line.split("\t");
		// finish read part

		String name = details[0];

		// create mapper
		context.write(new Text(name), new Text(details[1]));
		// end mapper
	}
}