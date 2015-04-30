
import java.io.FileInputStream;

import org.apache.mahout.math.Vector;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.UnsupportedEncodingException;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Random;
import java.util.Iterator;







import org.apache.mahout.classifier.evaluation.Auc;
//import org.apache.commons.math.util.OpenIntToDoubleHashMap.Iterator;
import org.apache.mahout.classifier.sgd.AdaptiveLogisticRegression;
import org.apache.mahout.classifier.sgd.CrossFoldLearner;
import org.apache.mahout.classifier.sgd.L1;
import org.apache.mahout.classifier.sgd.ModelSerializer;
import org.apache.mahout.classifier.sgd.OnlineLogisticRegression;
import org.apache.mahout.common.RandomUtils;
import org.apache.mahout.math.DenseVector;
import org.apache.mahout.math.RandomAccessSparseVector;
import org.apache.mahout.vectorizer.encoders.ConstantValueEncoder;
import org.apache.mahout.vectorizer.encoders.Dictionary;
import org.apache.mahout.vectorizer.encoders.FeatureVectorEncoder;
import org.apache.mahout.vectorizer.encoders.StaticWordValueEncoder;

import com.google.common.base.Charsets;
import com.google.common.base.Splitter;
import com.google.common.collect.Iterables;
import com.google.common.collect.Lists;
import com.google.common.collect.Maps;
import com.google.common.io.Resources;
//import javax.annotation.Resources;

public class LogisticRegression
{
	public static void main(String[] args) throws IOException {
		LogisticRegression logisticRegression = new LogisticRegression();
		List<Observation> trainingData = logisticRegression.parseInputFile("alldata");
		OnlineLogisticRegression olr = logisticRegression.train(trainingData);
		logisticRegression.testModel(olr);
	}
	
	public List<Observation> parseInputFile(String inputFile) {
		List<Observation> result = new ArrayList<Observation>();
		BufferedReader br = null;
		String line = "";
		try {
			br = new BufferedReader(new FileReader(new File(inputFile)));
			line = br.readLine();
			while ((line = br.readLine()) != null) {
				String[] values = line.split("	");
				result.add(new Observation(values));
			}}
		catch (FileNotFoundException e) {
				e.printStackTrace();
	    } catch (IOException e) {
				e.printStackTrace();
	    } finally {
			if (br != null) {
				try {
					br.close();
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
		return result;
	}
	
	public OnlineLogisticRegression train(List<Observation> trainData) {
		//
		OnlineLogisticRegression olr = new OnlineLogisticRegression(2, 11, new L1());
		//
		for (int pass = 0; pass <= 20; pass++) {
			for (Observation observation : trainData) {
				olr.train(observation.getActual(), observation.getVector());
			}
			if (pass % 10 == 0) {
				Auc eval = new Auc(0.5);
				for (Observation observation : trainData) {
					eval.add(observation.getActual(), olr.classifyScalar(observation.getVector()));
				}
				System.out.format("Pass: %2d,  Learning rate: %2.4f, Accuracy: %2.4f\n", pass, olr.currentLearningRate(), eval.auc());
				}
		}
		return olr;
	}
	
	void testModel(OnlineLogisticRegression olr) throws IOException {
		BufferedReader br = new BufferedReader(new InputStreamReader(new FileInputStream("2014")));
		PrintWriter pw = new PrintWriter("output","UTF-8" );
		String line;
		while((line = br.readLine())!= null) {
			String[] holder = line.split("	");
			Observation newObservation = new Observation(new String[] {"0",holder[1], holder[2], holder[3], holder[4], holder[5], holder[6], holder[7], holder[8], holder[9], holder[10]});
			Vector result = olr.classifyFull(newObservation.getVector());
			//System.out.println("------------Testing -----------");
			pw.print(holder[0]);
			pw.format("	%.3f\n", result.get(1));
			//System.out.format("Probability of decreasing/negtive revenue(0, args) = %.3f\n", result.get(0));
			//System.out.format("probability of increasing revenue(1) = %.3f\n", result.get(1));
		}
		pw.close();
		br.close();
	}
	
	class Observation {
		private DenseVector vector = new DenseVector(11);
		private int actual;
		
		public Observation(String[] values) {
			ConstantValueEncoder interceptEncoder  = new ConstantValueEncoder("intercept");
			StaticWordValueEncoder encoder = new StaticWordValueEncoder("feature");
			interceptEncoder.addToVector("1", vector);
			vector.set(1,  Double.valueOf(values[1]));
			vector.set(2,  Double.valueOf(values[2]));
			vector.set(3, Double.valueOf(values[3]));
			vector.set(4, Double.valueOf(values[4]));
			vector.set(5, Double.valueOf(values[5]));
			vector.set(6, Double.valueOf(values[6]));
			vector.set(7, Double.valueOf(values[7]));
			vector.set(8, Double.valueOf(values[8]));
			vector.set(9,  Double.valueOf(values[9]));
			vector.set(10, Double.valueOf(values[10]));
			encoder.addToVector(values[0], vector);
			this.actual = Integer.valueOf(values[0]);
		}
		
		public Vector getVector() {
			return vector;
		}
		
		public int getActual() {
			return actual;
		}
	}
}