import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;


public class Datecorrelation {
	public IntWritable score;
	public Text date;
	public Datecorrelation(String date, int score) {
		this.date=new Text(date);
		this.score= new IntWritable(score);
	}
}
