import spacy
from spacy.language import Language
from spacy_langdetect import LanguageDetector
from tqdm import tqdm


def get_df_models_and_labels(df, sep_str=" "):
    df_labels = df.drop(columns="category", axis=1)
    df_labels.reset_index(inplace=True)
    df_labels.drop(columns="glossary_link_id", axis=1, inplace=True)
    df_labels.drop(columns="element_id", axis=1, inplace=True)
    df_labels.label = df_labels.label.apply(lambda x: str(x or ''))
    df_labels.drop_duplicates(ignore_index=True, inplace=True)
    df_labels['label'] = df_labels.groupby(['model_id'])['label'].transform(lambda x: sep_str.join(x))
    df_labels.drop_duplicates(ignore_index=True, inplace=True)
    return df_labels.set_index("model_id")


def clean(label):
    # handle some special cases
    label = label.replace("\n", " ").replace("\r", "")
    # delete unnecessary whitespaces
    label = label.strip()
    return label


def get_lang_detector(nlp, name):
    return LanguageDetector()


class ModelLanguageDetector:
    def __init__(self, threshold):
        self.threshold = threshold
        self.nlp = spacy.load("en_core_web_sm")
        Language.factory("language_detector", func=get_lang_detector)
        self.nlp.add_pipe('language_detector', last=True)

    def _get_text_language(self, text):
        doc = self.nlp(str(clean(text)))
        detection = doc._.language
        return detection['language']

    def add_detected_natural_language_from_meta(self, df_meta):
        df_meta['detected_natural_language'] = [self._get_text_language(name) for name in tqdm(df_meta.name)]

    def get_detected_natural_language_from_bpmn_model(self, df):
        df_labels = get_df_models_and_labels(df, " ")
        df_labels['detected_natural_language'] = [self._get_text_language(label) for label in tqdm(df_labels.label)]
        return df_labels
