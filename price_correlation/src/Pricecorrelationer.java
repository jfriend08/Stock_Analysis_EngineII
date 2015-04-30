import org.apache.hadoop.mapred.JobConf;
import org.apache.hadoop.mapred.jobcontrol.JobControl;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured; 
import org.apache.hadoop.fs.Path; 
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text; 
import org.apache.hadoop.mapreduce.Job; 
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat; 
import org.apache.hadoop.mapreduce.lib.jobcontrol.ControlledJob;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat; 
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner; 
/*This class is responsible for running map reduce job*/

public class Pricecorrelationer extends Configured implements Tool {

	public int run(String[] args) throws Exception {

    /*
     * Validate that two arguments were passed from the command line.
     */
    if (args.length != 3) {
      System.out.printf("Usage: StubDriver <input dir> <temp dir> <output dir>\n");
      System.exit(-1);
    }

    /*
     * Instantiate a Job object for your job's configuration. 
     */
    JobConf conf = new JobConf(Pricecorrelationer.class);
    Job job1 = new Job(conf,"join1");
    
    /*
     * Specify the jar file that contains your driver, mapper, and reducer.
     * Hadoop will transfer this jar file to nodes in your cluster running 
     * mapper and reducer tasks.
     */
    job1.setJarByClass(Pricecorrelationer.class);
    FileInputFormat.addInputPath(job1, new Path(args[0])); 
    FileOutputFormat.setOutputPath(job1,new Path(args[1]));
    /*
     * Specify an easily-decipherable name for the job.
     * This job name will appear in reports and logs.
     */
    job1.setMapperClass(StubMapper.class); 
    job1.setReducerClass(StubReducer.class);
//    job.setReducerClass(ReducetoAll.class);
//    job.setJobName("Stub Driver");

    /*
     * TODO implement
     */
    job1.setOutputKeyClass(Text.class); 
    job1.setOutputValueClass(Text.class); 
    
    ControlledJob ctrljob1= new ControlledJob(conf);
    ctrljob1.setJob(job1);
    
    JobControl jobCtrl=new JobControl("myctrl"); 
    
    jobCtrl.addJob(ctrljob1); 
    boolean success = job1.waitForCompletion(true); 
    
    JobConf conf2 = new JobConf(Pricecorrelationer.class);
    Job job2 = new Job(conf,"join1");
    
    job2.setJarByClass(Pricecorrelationer.class);
    FileInputFormat.addInputPath(job2, new Path(args[1])); 
    FileOutputFormat.setOutputPath(job2,new Path(args[2]));
    /*
     * Specify an easily-decipherable name for the job.
     * This job name will appear in reports and logs.
     */
    job2.setMapperClass(Mapper2.class); 
    job2.setReducerClass(ReducetoAll.class);
//    job.setJobName("Stub Driver");

    /*
     * TODO implement
     */
    job2.setOutputKeyClass(Text.class); 
    job2.setOutputValueClass(Text.class); 
    
    
//    System.exit(job1.waitForCompletion(true) ? 0:1);  
    success = job2.waitForCompletion(true); 
    
    return success ? 0 : 1; 
    /*
     * Start the MapReduce job and wait for it to finish.
     * If it finishes successfully, return 0. If not, return 1.
     */
  }
	public static void main(String[] args) throws Exception { 
		Pricecorrelationer driver = new Pricecorrelationer(); 
		int exitCode = ToolRunner.run(driver, args); 
		System.exit(exitCode); 
		}
}

