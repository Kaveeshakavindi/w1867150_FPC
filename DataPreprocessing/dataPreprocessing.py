# dataPreprocessing.py

# 1. input preparation: The document is first split into its constituent sentences
<<<<<<< HEAD
# 2. Sentence encoding – Each sentence is passed through a pre‑trained sentence encoder (e.g., SBERT, InferSent, LASER, USE). The encoder outputs a fixed‑size vector for every sentence 
=======
# 2. Sentence encoding – Each sentence is passed through a pre‑trained sentence encoder 
>>>>>>> c6f1b0fed3f17a5ced5ccef3c48defb6b72336ee
# 3. topic encoding – Topics are encoded in one of four ways:
# * Name‑Only (just the topic phrase)
# * Name + Keywords (average of topic name and its keywords)
# * Topic + Keyword + Definition (uses WordNet definitions)
# * Explicit‑Mentions (averages embeddings of articles that explicitly contain the topic)  .
# The “Explicit‑Mentions” + “Entire Article” combo gave the strongest results
# 4. ex-tracted the informative keywords for each topicusing the TF-IDF heuristics. Then, a set of key-words for each topic were selected through carefulinspection of the top keywords with high TF-IDFscores.
# 5. Similarity matching - Cosine similarity is computed between every sentence vector and each topic vector 

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import wordnet as wn
import time
from typing import Dict, List, Tuple
import re
import csv
from datetime import datetime
import sys

max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = max_int // 10


nltk.download('wordnet', quiet=True)
nltk.download('punkt', quiet=True)

class ESGSentenceExtractor:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Initialize the ESG sentence extractor with a sentence transformer model.
        """
        self.model = SentenceTransformer(model_name)
        self.esg_topic_keywords = {}
        self.esg_topic_embeddings = {}
        
    # step 1 : clean and normalize text
    def preprocess_text(self, text: str) -> str:
        text = re.sub(r'\s+', ' ', text) #replace multiple spaces with single space
        text = re.sub(r'[^\w\s\.\,\!\?\-]', '', text) #remove special characters except basic punctuation
        return text.strip() #remove leading/trailing spaces
    
    # step 2 : Split document into sentences
    def split_sentences(self, document: str) -> List[str]:
        document = self.preprocess_text(document)
        sentences = nltk.sent_tokenize(document)
        return [s for s in sentences if len(s.split()) > 3]
    
    # step 3 : Convert CamelCase to words
    def camel_case_to_words(self, topic: str) -> str:
        words = re.sub(r'([A-Z])', r' \1', topic).strip()
        return words.lower()
    
    # step 4 : Generate synonyms for topic words using WordNet
    def generate_topic_synonyms(self, topic: str) -> List[str]:
        words = self.camel_case_to_words(topic).split()
        synonyms = []
        
        for word in words:
            synsets = wn.synsets(word)
            for syn in synsets[:2]: 
                for lemma in syn.lemmas():
                    synonym = lemma.name().replace('_', ' ')
                    if synonym not in synonyms and synonym != word:
                        synonyms.append(synonym)
        
        return synonyms[:5] 
    
    
    def extract_topic_keywords_from_content(self, content: str, topics: List[str], 
                                           n_keywords: int = 10) -> Dict[str, List[str]]:
        """
        Extract relevant keywords for each ESG topic from the document content.
        Uses TF-IDF with topic-specific filtering.
        """
        sentences = self.split_sentences(content)
        topic_keywords = {}
        
        for topic in topics:
            # Convert topic to readable words
            topic_words = self.camel_case_to_words(topic)
            topic_terms = set(topic_words.split())
            
            # Add synonyms
            synonyms = self.generate_topic_synonyms(topic)
            topic_terms.update(synonyms)
            
            #find sentences that mention topic-related terms
            relevant_sentences = []
            for sent in sentences:
                sent_lower = sent.lower()
                if any(term in sent_lower for term in topic_terms):
                    relevant_sentences.append(sent)
            
            if not relevant_sentences:
                # if no direct matches, use the original topic words
                topic_keywords[topic] = [topic_words] + synonyms
                continue
            
            #relevent sentences = sentences that directly mention original esg topic/s or synonyms
            #extract keywords using TF-IDF from relevant sentences
            #it extracts keywords that are frequesnt in relevant sentences
            try:
                vectorizer = TfidfVectorizer(
                    max_features=n_keywords * 2,
                    stop_words='english', #ignores common english words like 'the', 'is'
                    ngram_range=(1, 3),  #consider unigrams, bigrams and trigrams
                    min_df=1 #include any term that appears in atleast one sentence

                    # unigram: eg: 'green'
                    # bigram: eg: 'green energy'
                    # trigram : eg: 'green energy policy'
                )
                
                tfidf_matrix = vectorizer.fit_transform(relevant_sentences)
                feature_names = vectorizer.get_feature_names_out()
                
                #top n keywords with the heighest TF-IDF score is selected
                scores = tfidf_matrix.sum(axis=0).A1 
                top_indices = scores.argsort()[-n_keywords:][::-1]
                keywords = [feature_names[i] for i in top_indices]
                
                #combine with topic words, synonyms and TF-IDF keywords
                all_keywords = [topic_words] + keywords + synonyms
                topic_keywords[topic] = list(dict.fromkeys(all_keywords))[:n_keywords] #ensures unique keywords
                
            except Exception as e:
                #fallback to topic words and synonyms
                topic_keywords[topic] = [topic_words] + synonyms
        
        return topic_keywords
    
    def build_topic_context(self, topic: str, keywords: List[str], 
                           content: str) -> List[str]:
        """
        Build context for a topic by finding sentences that mention the topic or its keywords.
        This simulates the "explicit mentions" approach from the paper.
        """
        sentences = self.split_sentences(content)
        context_sentences = []
        
        # Convert topic and keywords to lowercase for matching
        topic_lower = self.camel_case_to_words(topic).lower()
        keywords_lower = [kw.lower() for kw in keywords]
        
        for sent in sentences:
            sent_lower = sent.lower()
            # Check if sentence mentions topic or keywords
            if (topic_lower in sent_lower or 
                any(kw in sent_lower for kw in keywords_lower)):
                context_sentences.append(sent)
        
        return context_sentences[:10]  # Limit context sentences
    
    def encode_topic_with_context(self, topic: str, keywords: List[str], 
                                  context_sentences: List[str]) -> np.ndarray:
        """
        Encode topic using explicit mentions approach.
        """
        # Create topic-enriched context
        topic_phrase = self.camel_case_to_words(topic)
        
        texts_to_encode = [
            topic_phrase,  # Original topic
            f"{topic_phrase}: {' '.join(keywords[:5])}"  # Topic with keywords
        ]
        
        # Add context sentences with topic prepended
        for sent in context_sentences[:5]:
            texts_to_encode.append(f"{topic_phrase}. {sent}")
        
        # Encode all texts
        embeddings = self.model.encode(texts_to_encode)
        
        # Weighted average: give more weight to topic with keywords
        weights = np.array([2.0, 3.0] + [1.0] * len(context_sentences[:5]))
        weights = weights / weights.sum()
        
        return np.average(embeddings, axis=0, weights=weights[:len(embeddings)])
    
    def extract_esg_sentences(self, content: str, esg_topics: List[str], 
                             threshold: float = 0.3, 
                             top_k: int = 5) -> Dict[str, List[Tuple[str, float]]]:
        """
        Extract sentences from content that match ESG topics.
        
        Args:
            content: Document content
            esg_topics: List of ESG topic names (CamelCase)
            threshold: Minimum similarity threshold (0-1)
            top_k: Number of top sentences to return per topic
            
        Returns:
            Dictionary mapping topics to list of (sentence, similarity_score) tuples
        """
        # Step 1: Extract keywords for each topic from the content
        print("Extracting topic-specific keywords...")
        topic_keywords = self.extract_topic_keywords_from_content(content, esg_topics)
        
        # Step 2: Build context for each topic
        print("Building topic contexts...")
        topic_contexts = {}
        for topic, keywords in topic_keywords.items():
            context = self.build_topic_context(topic, keywords, content)
            topic_contexts[topic] = context
        
        # Step 3: Encode topics with their context
        print("Encoding topics...")
        topic_embeddings = {}
        for topic, keywords in topic_keywords.items():
            context = topic_contexts[topic]
            if context:  # Only encode if we have context
                embedding = self.encode_topic_with_context(topic, keywords, context)
                topic_embeddings[topic] = embedding
        
        # Step 4: Encode all sentences in the document
        print("Encoding sentences...")
        sentences = self.split_sentences(content)
        if not sentences:
            return {}
        
        sentence_embeddings = self.model.encode(sentences)
        
        # Step 5: Compute similarities and extract matching sentences
        print("Computing similarities...")
        results = {}
        
        for topic, topic_embedding in topic_embeddings.items():
            # Compute cosine similarity
            topic_embedding = topic_embedding.reshape(1, -1)
            similarities = cosine_similarity(sentence_embeddings, topic_embedding).flatten()
            
            # Get sentences above threshold
            matching_indices = np.where(similarities >= threshold)[0]
            
            if len(matching_indices) > 0:
                # Sort by similarity and get top_k
                sorted_indices = matching_indices[np.argsort(similarities[matching_indices])[::-1]]
                top_indices = sorted_indices[:top_k]
                
                matches = [
                    (sentences[idx], float(similarities[idx])) 
                    for idx in top_indices
                ]
                
                results[topic] = {
                    'matches': matches,
                    'keywords': topic_keywords[topic],
                    'total_matches': len(matching_indices)
                }
        
        return results
    
    def process_dataframe_row(self, row: pd.Series, threshold: float = 0.3, 
                             top_k: int = 5) -> Dict:
        """
        Process a single row from the dataframe.
        
        Args:
            row: Pandas Series containing 'content' and 'esg_topics'
            threshold: Minimum similarity threshold
            top_k: Number of top sentences per topic
            
        Returns:
            Dictionary with extraction results
        """
        content = row['content']
        esg_topics = eval(row['esg_topics']) if isinstance(row['esg_topics'], str) else row['esg_topics']
        
        return self.extract_esg_sentences(content, esg_topics, threshold, top_k)
    
    
def results_to_csv(results: Dict, output_file: str = None, include_scores: bool = True):
        """
        Convert extraction results to CSV format.
        
        Args:
            results: Dictionary from extract_esg_sentences()
            output_file: Path to output CSV file (optional)
            include_scores: Whether to include similarity scores in the output
        
        Returns:
            DataFrame with the results
        """
        # Prepare data for CSV
        csv_data = []
        
        for topic, data in results.items():
            for sentence, score in data['matches']:
                row = {
                    'esg_topic': topic,
                    'sentence': sentence.strip(),
                    'similarity_score': round(score, 4) if include_scores else None,
                    'keywords': '; '.join(data['keywords'][:5])
                }
                csv_data.append(row)
        
        # Create DataFrame
        df = pd.DataFrame(csv_data)
        
        # Generate filename if not provided
        if output_file is None:
            output_file = f'esg_extraction_results.csv'
        
        # Write to CSV
        if include_scores:
            df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
        else:
            df[['esg_topic', 'sentence']].to_csv(output_file, index=False, 
                                                encoding='utf-8', quoting=csv.QUOTE_ALL)
        
        print(f"\nResults saved to: {output_file}")
        print(f"Total rows: {len(df)}")
        print(f"Topics covered: {df['esg_topic'].nunique()}")

        return df

def process_csv_dataset(csv_path: str, output_dir: str = 'output', 
                        threshold: float = 0.35, top_k: int = 5):
    """
    Process entire CSV dataset and extract ESG sentences for each document.
    
    Args:
        csv_path: Path to the CSV file containing 'content' and 'esg_topics' columns
        output_dir: Directory to save output files
        threshold: Minimum similarity threshold
        top_k: Number of top sentences per topic
    """
    import os
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Load dataset
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(
        csv_path,
        sep='|',             
        quotechar='"',
        engine='python',
        encoding='utf-8'
    )
    
    print(f"Dataset loaded: {len(df)} records")
    print(f"Columns: {list(df.columns)}")
    
    # Verify required columns exist
    if 'content' not in df.columns or 'esg_topics' not in df.columns:
        raise ValueError("CSV must contain 'content' and 'esg_topics' columns")
    
    # Initialize extractor
    extractor = ESGSentenceExtractor()
    
    # Process each document
    all_results = []
    failed_records = []
    
    print("\n" + "="*80)
    print("PROCESSING DATASET")
    print("="*80 + "\n")
    
    for idx, row in df.iterrows():
        try:
            print(f"Processing record {idx + 1}/{len(df)}...")
            content = row['content']
            if isinstance(row['esg_topics'], str):
                topics_str = row['esg_topics'].strip('[]').replace("'", "").replace('"', '')
                esg_topics = [t.strip() for t in topics_str.split(',') if t.strip()]
            else:
                esg_topics = row['esg_topics']
            
            if not content or not esg_topics:
                print(f"Skipping - empty content or topics")
                failed_records.append({'index': idx, 'reason': 'empty_data'})
                continue
            
            #extract ESG sentences
            results = extractor.extract_esg_sentences(
                content=content,
                esg_topics=esg_topics,
                threshold=threshold,
                top_k=top_k
            )
            
            # Add metadata to results
            for topic, data in results.items():
                for sentence, score in data['matches']:
                    all_results.append({
                        'record_index': idx,
                        'company': row.get('company', 'Unknown'),
                        'date': row.get('date', 'Unknown'),
                        'title': row.get('title', 'Unknown'),
                        'url': row.get('url', 'Unknown'),
                        'esg_topic': topic,
                        'sentence': sentence.strip(),
                        'similarity_score': round(score, 4),
                        'keywords': '; '.join(data['keywords'][:5])
                    })
            
            print(f"Extracted {len(results)} topics with matches")
            
        except Exception as e:
            print(f"Error processing record {idx}: {str(e)}")
            failed_records.append({'index': idx, 'reason': str(e)})
            continue
    
    # Create results DataFrame
    results_df = pd.DataFrame(all_results)
    
    # Save results
    output_file = os.path.join(output_dir, f'esg_extraction_results.csv')
    results_df.to_csv(output_file, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)
    
    # Save failed records
    if failed_records:
        failed_file = os.path.join(output_dir, f'failed_records.csv')
        pd.DataFrame(failed_records).to_csv(failed_file, index=False)
        print(f"\nFailed records saved to: {failed_file}")
    
    # Print summary
    print("\n" + "="*80)
    print("PROCESSING COMPLETE")
    print("="*80)
    print(f"Results saved to: {output_file}")
    print(f"Total sentences extracted: {len(results_df)}")
    print(f"Total records processed: {len(df)}")
    print(f"Failed records: {len(failed_records)}")
    print(f"Topics covered: {results_df['esg_topic'].nunique()}")
    print(f"Companies covered: {results_df['company'].nunique()}")

    # Print topic distribution
    print("\nTopic Distribution:")
    topic_counts = results_df['esg_topic'].value_counts()
    for topic, count in topic_counts.head(10).items():
        print(f"   {topic}: {count}")
    
    return results_df, failed_records


if __name__ == '__main__':

    # Configuration
    FILE_PATH = "Dataset/raw/esg_documents_for_dax_companies.csv"
    OUTPUT_DIR = "Dataset/processed/semantic_extraction"
    THRESHOLD = 0.35  
    TOP_K = 5 
    
    # Process the entire dataset
    print("Starting ESG Sentence Extraction Pipeline")
    print("="*80)
    
    try:
        results_df, failed_records = process_csv_dataset(
            csv_path=FILE_PATH,
            output_dir=OUTPUT_DIR,
            threshold=THRESHOLD,
            top_k=TOP_K
        )
        
        # Display sample results
        print("\n" + "="*80)
        print("SAMPLE RESULTS")
        print("="*80)
        print(results_df.head(10))
        
        # Display statistics by company
        print("\n" + "="*80)
        print("RESULTS BY COMPANY")
        print("="*80)
        company_stats = results_df.groupby('company').agg({
            'sentence': 'count',
            'esg_topic': 'nunique',
            'similarity_score': 'mean'
        }).round(3)
        company_stats.columns = ['Total Sentences', 'Unique Topics', 'Avg Score']
        print(company_stats)
        
    except Exception as e:
        print(f"\n Error: {str(e)}")
        print("Please ensure:")
        print("  1. CSV file exists at the specified path")
        print("  2. CSV contains 'content' and 'esg_topics' columns")
        print("  3. You have write permissions for the output directory")