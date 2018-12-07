package be.inqa.phd.hivhack.data;

import static org.junit.Assert.*;

import java.io.BufferedOutputStream;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStreamWriter;
import java.util.List;

import org.apache.commons.compress.compressors.FileNameUtil;
import org.apache.commons.io.FilenameUtils;
import org.apache.commons.io.IOUtils;
import org.apache.uima.UIMAException;
import org.apache.uima.analysis_engine.AnalysisEngineDescription;
import org.apache.uima.collection.CollectionReader;
import org.apache.uima.fit.component.CasDumpWriter;
import org.apache.uima.fit.factory.AnalysisEngineFactory;
import org.apache.uima.fit.factory.CollectionReaderFactory;
import org.apache.uima.fit.pipeline.SimplePipeline;
import org.apache.uima.resource.ResourceInitializationException;
import org.junit.Test;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;

import de.tudarmstadt.ukp.dkpro.core.io.text.TextReader;
import de.tudarmstadt.ukp.dkpro.core.io.text.TextWriter;
import de.tudarmstadt.ukp.dkpro.core.stanfordnlp.StanfordSegmenter;
import de.tudarmstadt.ukp.dkpro.core.tokit.BreakIteratorSegmenter;
import lombok.extern.log4j.Log4j;

@Log4j
public class GazetteNoticeTest {

	static final String DIR_TEST = new File(GazetteNoticeTest.class.getResource("sample.json").getPath()).getParent();

	@Test
	public void testJson() throws IOException {
//		InputStream is = GazetteNoticeTest.class.getResourceAsStream("sample.json");
//		String directory = new File(GazetteNoticeTest.class.getResource("sample.json").getPath()).getParent();
		InputStream is = new FileInputStream(new File("/Users/Joachim/Documents/Inqa/2018-HIVHACK/data-artverc/data-gazette-kenya/items.json"));
		byte[] bytes = IOUtils.toByteArray(is);
		ObjectMapper objectMapper = new ObjectMapper();
		List<GazetteNotice> list = objectMapper.readValue(bytes, new TypeReference<List<GazetteNotice>>() {
		});
		OutputStreamWriter writer = new OutputStreamWriter(
				new FileOutputStream("/Users/Joachim/Documents/Inqa/2018-HIVHACK/data-artverc/data-gazette-kenya/itmes.txt"), "UTF-8");
		for (GazetteNotice gazette : list) {
			String raw = gazette.getText();
			
			raw = raw.replaceAll("(?m)^[ \t]*\r?\n", "");
			raw = raw.trim();
			if (!raw.isEmpty()) {
				log.info(raw);
				writer.write(raw);
			}
		}
		writer.close();
	}

	@Test
	public void testUima() throws UIMAException, IOException {
		CollectionReader reader = CollectionReaderFactory.createReader(TextReader.class,
				TextReader.PARAM_SOURCE_LOCATION, DIR_TEST, TextReader.PARAM_LANGUAGE, "en", TextReader.PARAM_PATTERNS,
				new String[] { "[+]*.txt" });
		

		
		AnalysisEngineDescription segmenter = AnalysisEngineFactory.createEngineDescription(
				BreakIteratorSegmenter.class, BreakIteratorSegmenter.PARAM_WRITE_TOKEN, false,
				BreakIteratorSegmenter.PARAM_WRITE_SENTENCE, true);
		
		 AnalysisEngineDescription segmenterSt = AnalysisEngineFactory.createEngineDescription(StanfordSegmenter.class,
		 StanfordSegmenter.PARAM_ALLOW_EMPTY_SENTENCES, false);
		
		 AnalysisEngineDescription writer = AnalysisEngineFactory.createEngineDescription(TextWriter.class,
				 TextWriter.PARAM_TARGET_ENCODING, "UTF-8",
				 TextWriter.PARAM_OVERWRITE, true,
				 TextWriter.PARAM_TARGET_LOCATION, FilenameUtils.concat(DIR_TEST, "sample-segmented"));
		
//		AnalysisEngineDescription writer = AnalysisEngineFactory.createEngineDescription(TextWriter.class);

		SimplePipeline.runPipeline(reader, segmenter, segmenterSt, writer);
		log.info(FilenameUtils.concat(DIR_TEST, "sample-segmented"));

	}

}
