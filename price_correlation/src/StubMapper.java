import java.io.IOException;
import java.util.StringTokenizer;

import org.apache.commons.math3.util.Decimal64;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class StubMapper extends Mapper<LongWritable, Text, Text, Text> {

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

		double open = Double.parseDouble(details[2]);
		double close = Double.parseDouble(details[5]);

		// create mapper
		if (open - close >= 0) {
			context.write(new Text(details[1]), new Text(details[0] + ":-"));
		} else {
			context.write(new Text(details[1]), new Text(details[0] + ":+"));
		}
		// end mapper
	}
}
