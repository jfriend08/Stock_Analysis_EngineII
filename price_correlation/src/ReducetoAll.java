import java.io.IOException;
import java.util.ArrayList;
import java.util.Collections;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.Reducer.Context;

public class ReducetoAll extends Reducer<Text, Text, Text, Text> {

	@Override
	public void reduce(Text key, Iterable<Text> values, Context context)
			throws IOException, InterruptedException {

		ArrayList<String> resultList = new ArrayList<String>();

		for (Text value : values) {
			resultList.add(value.toString());
		}

		Collections.sort(resultList);
		int total = 0;
		int count = 0;
		for (int i = resultList.size() - 1; i >= 0 && count < 180; i--) {
			count++;
			total += Integer.parseInt(resultList.get(i).split(":")[1]);
		}
		context.write(key, new Text(total + "\t" + count));
	}

}
