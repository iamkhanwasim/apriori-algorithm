import pandas as pd
from itertools import combinations

def generate_frequent_itemsets(df, min_support=0.5):
    """
    Implements Apriori algorithm to generate frequent itemsets from binary transaction data.
    
    Parameters:
    df (pd.DataFrame): A dataframe with binary values (0/1) where rows represent transactions and
                       columns represent items.
    min_support (float): Minimum support threshold.
    
    Returns:
    dict: A dictionary where keys are frequent itemsets (frozenset) and values are their support.
    """
    # Number of transactions
    num_transactions = len(df)
    
    # Step 1: Find frequent 1-itemsets
    item_support = {}
    for column in df.columns:
        
        # print(type(int(df[column].sum())))
        # print(type(num_transactions))
        support = df[column].sum() / num_transactions
        if support >= min_support:
            item_support[frozenset([column])] = support
    
    # Initialize the frequent itemsets with frequent 1-itemsets
    frequent_itemsets = item_support.copy()
    print(frequent_itemsets)
    # return 0
    # Step 2: Generate candidate itemsets of size k and filter by min_support
    k = 2
    current_itemsets = list(item_support.keys())
    
    while current_itemsets:
        # Generate candidate itemsets of size k by combining k-1 itemsets
        candidate_itemsets = []
        for i in range(len(current_itemsets)):
            for j in range(i + 1, len(current_itemsets)):
                candidate = current_itemsets[i].union(current_itemsets[j])
                if len(candidate) == k:
                    candidate_itemsets.append(candidate)
        
        # Calculate support for candidate itemsets
        candidate_support = {}
        for candidate in candidate_itemsets:
            # Check how many transactions contain this candidate
            support = df[list(candidate)].all(axis=1).sum() / num_transactions
            if support >= min_support:
                candidate_support[frozenset(candidate)] = support
        
        # Add frequent k-itemsets to the result
        frequent_itemsets.update(candidate_support)
        
        # Prepare for the next iteration (generate k+1 itemsets)
        current_itemsets = list(candidate_support.keys())
        k += 1
    
    return frequent_itemsets

# frequent_itemsets = generate_frequent_itemsets(basket, 0.1)

def generate_rules_3(frequent_itemsets, min_confidence=0.5, max_antecedent=2, max_consequent=2):
    """
    Generate association rules from frequent itemsets along with confidence, lift, and support metrics.
    
    Parameters:
    frequent_itemsets (dict): Dictionary where keys are itemsets (frozenset) and values are their support.
    min_confidence (float): Minimum confidence threshold for filtering rules.
    max_antecedent (int): Maximum number of items allowed in the antecedent.
    max_consequent (int): Maximum number of items allowed in the consequent.
    
    Returns:
    pd.DataFrame: A DataFrame of rules with antecedent, consequent, confidence, lift, and support.
    """
    rules = []
    itemsets = list(frequent_itemsets.keys())
    
    for itemset in itemsets:
        if len(itemset) > 1:
            # For each frequent itemset, generate all possible non-empty proper subsets (A)
            for i in range(1, min(max_antecedent, len(itemset)) + 1):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent
                    
                    if consequent and len(consequent) <= max_consequent:
                        # Calculate confidence: P(A → B) = support(A ∪ B) / support(A)
                        confidence = frequent_itemsets[itemset] / frequent_itemsets[antecedent]
                        
                        # Only consider rules with confidence greater than or equal to min_confidence
                        if confidence >= min_confidence:
                            # Calculate lift: Lift(A → B) = confidence(A → B) / support(B)
                            lift = confidence / frequent_itemsets[frozenset(consequent)]
                            
                            # Get support for the full itemset (antecedent ∪ consequent)
                            support = frequent_itemsets[itemset]
                            
                            # Convert sets to strings for display without brackets
                            rules.append({
                                'antecedent': ', '.join(antecedent),
                                'consequent': ', '.join(consequent),
                                'confidence': confidence,
                                'lift': lift,
                                'support': support
                            })
    
    # Convert the list of rules to a DataFrame
    return pd.DataFrame(rules)

if __name__ == "__main__":    
    basket = pd.DataFrame({ 
        'bread': [1, 1, 0, 0, 1],
        'butter': [1, 1, 1, 1, 1],
        'coffee': [0, 1, 1, 1, 1],
        'milk': [1, 1, 1, 1, 1],
        'sugar': [0, 1, 0, 1, 0]})
    # print(basket)
    frequent_itemsets = generate_frequent_itemsets(basket, 0.1)
    rules_df = generate_rules_3(frequent_itemsets, 0,5,5)
    print(frequent_itemsets)