import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;
import java.io.IOException;

public class MergeReducer extends Reducer<Text, Text, Text, Text>{
	public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
		String[] str = new String[6];
		for(Text value : values) {
			String[] holder = value.toString().split("	");
			int position = Integer.valueOf(holder[0]);
			str[position - 1] = holder[1];
		}
		
		StringBuilder sb = new StringBuilder();
		sb.append(str[0]);
		for (int i = 1; i < 6; i++) {
			sb.append("	" + str[i]);
		}
		String value = sb.toString();
		
		
		context.write(key, new Text(value));
	}
}
