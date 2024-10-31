import pandas as pd

# Skrypt do czyszczenia danych
# Po przeprowadzdeniu EDA, zauważyłem, że:
# tags zawiera dużo wartości null, co może zafałszować dane i sprawić, że będą one stronnicze w kierunku wartości nie-nullowych
# ingredients zawiera listę słowników, każdy słownik zawiera składnik i jego metryki, z którego najważniejsza jest nazwa (ewentualnie to czy zawiera alkohol, jednak w kolumnie alcoholic mamy już tę informację)
# id, name, imageurl, created at i updated at nie są istotne do klastrowania
# instructions nie wydają się istotne, chyba że chcemy klastrować koktajle na bazie podobienstwa instrukcji, co wymagałoby dużo NLP

def clean_data(df):
    """
    Funkcja czyszcząca dane, przetwarzajaca dataframe do postaci, w której można przeprowadzić klastrowanie
    Input : df - dataframe pełny danych o koktajlach
    Output : df - dataframe gotowy do klastrowania zakodowany w postaci one-hot
    """
    df = df.copy()
    df.drop(['id', 'name', 'alcoholic', 'instructions', 'tags', 'imageUrl', 'createdAt', 'updatedAt'], axis=1, inplace=True)

    expanded_ingredients = df['ingredients'].apply(lambda x:[ingredient['name'] for ingredient in x])

    ingredients_df = expanded_ingredients.explode().str.get_dummies().groupby(level=0).sum()

    df['ingredient_count'] = df['ingredients'].apply(len)
    df.drop('ingredients', axis=1, inplace=True)


    glass_dummies = pd.get_dummies(df['glass'])
    df.drop('glass', axis=1, inplace=True)

    category_dummies = pd.get_dummies(df['category'])
    df.drop('category', axis=1, inplace=True)
    df = pd.concat([df, category_dummies, glass_dummies, ingredients_df], axis=1)
    
    return df


