import java.io.IOException;

import org.apache.hadoop.io.DoubleWritable;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;


public class SeekalphaReducer extends Reducer<Text, IntWritable, Text, DoubleWritable>{
	public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
		int count = 0;
		double score = 0;
		for(IntWritable value : values) {
			score = score + value.get();
			count ++;
		}
		score = score / count;
		context.write(key, new DoubleWritable(score));
	}
}
