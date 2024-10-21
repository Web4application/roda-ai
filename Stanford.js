import edu.stanford.nlp.pipeline.*;

public class StanfordNLPExample {
public static void main(String[] args) {
StanfordCoreNLP pipeline = new StanfordCoreNLP("StanfordCoreNLP.properties");
CoreDocument document = new CoreDocument("This is a simple NLP example.");
pipeline.annotate(document);

for (CoreLabel token : document.tokens()) {
System.out.println(token.word() + " - " + token.ner());
}
}
}
