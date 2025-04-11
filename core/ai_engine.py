from transformers import pipeline
import spacy

class AIEngine:
    def __init__(self):
        """
        Initialize AI Engine with required NLP models and pipelines.
        """
        # Load NLP models
        self.nlp = spacy.load("en_core_web_sm")
        
        # Initialize Transformers pipelines
        self.sentiment_analyzer = pipeline("sentiment-analysis")
        self.text_summarizer = pipeline("summarization")
        self.question_answering = pipeline("question-answering")

    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze the sentiment of the given text.
        Args:
            text (str): The input text.
        Returns:
            dict: Sentiment analysis result.
        """
        result = self.sentiment_analyzer(text)
        return result[0]  # Return the first result (most relevant)

    def summarize_text(self, text: str, max_length: int = 50, min_length: int = 25) -> str:
        """
        Summarize the given text.
        Args:
            text (str): The input text to summarize.
            max_length (int): Maximum length of the summary.
            min_length (int): Minimum length of the summary.
        Returns:
            str: The summarized text.
        """
        summary = self.text_summarizer(text, max_length=max_length, min_length=min_length, do_sample=False)
        return summary[0]["summary_text"]

    def extract_entities(self, text: str) -> dict:
        """
        Extract named entities from the given text.
        Args:
            text (str): The input text.
        Returns:
            dict: Dictionary containing entities and their types.
        """
        doc = self.nlp(text)
        entities = {ent.text: ent.label_ for ent in doc.ents}
        return entities

    def answer_question(self, question: str, context: str) -> str:
        """
        Answer a question based on the given context.
        Args:
            question (str): The question to answer.
            context (str): The context to use for answering.
        Returns:
            str: The answer to the question.
        """
        result = self.question_answering(question=question, context=context)
        return result["answer"]

    def process_user_query(self, query: str, context: str = None) -> dict:
        """
        Process a general user query.
        Args:
            query (str): The user's query.
            context (str): Optional context for the query.
        Returns:
            dict: Results of processed query including sentiment, entities, and summary.
        """
        result = {
            "sentiment": self.analyze_sentiment(query),
            "entities": self.extract_entities(query),
        }

        if context:
            result["answer"] = self.answer_question(query, context)

        result["summary"] = self.summarize_text(query)
        return result