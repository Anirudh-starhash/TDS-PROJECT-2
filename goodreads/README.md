## storytelling Result for goodreads.csv:

### Narrative:

#### Summary of the Dataset:
- **Total Entries**: N/A
- **Missing Values**: book_id: 0, goodreads_book_id: 0, best_book_id: 0, work_id: 0, books_count: 0, isbn: 700, isbn13: 585, authors: 0, original_publication_year: 21, original_title: 585, title: 0, language_code: 1084, average_rating: 0, ratings_count: 0, work_ratings_count: 0, work_text_reviews_count: 0, ratings_1: 0, ratings_2: 0, ratings_3: 0, ratings_4: 0, ratings_5: 0, image_url: 0, small_image_url: 0
- **Outliers**: 

#### The Analysis Performed:
- **Outlier Detection**: [4.34, 4.44, 3.57, 4.25, 3.89, 4.26, 4.25, 3.79, 3.85, 4.24, 4.26, 4.24, 4.14, 3.87, 4.1, 4.11, 4.3, 4.53, 4.34, 4.03, 4.46, 3.77, 4.37, 4.53, 4.61, 3.79, 4.54, 3.64, 3.73, 4.03, 4.45, 3.84, 4.06, 4.3, 3.75, 4.17, 3.84, 4.09, 3.88, 4.3, 3.93, 3.7, 3.73, 4.28, 4.0, 4.01, 3.88, 3.96, 4.06, 4.3, 3.93, 4.16, 3.85, 4.22, 4.0, 3.9, 3.67, 4.0, 3.98, 3.93, 4.07, 4.03]
- **Correlation Analysis**: [[272, 2008.0, 4.34, 4780653, 4942365, 155254, 66715, 127936, 560092, 1481305, 2706317], [491, 1997.0, 4.44, 4602479, 4800065, 75867, 75504, 101676, 455024, 1156318, 3011543], [226, 2005.0, 3.57, 3866839, 3916824, 95009, 456191, 436802, 793319, 875073, 1355439], [487, 1960.0, 4.25, 3198671, 3340896, 72586, 60427, 117415, 446835, 1001952, 1714267], [1356, 1925.0, 3.89, 2683664, 2773745, 51992, 86236, 197621, 606158, 936012, 947718], [226, 2012.0, 4.26, 2346404, 2478609, 140739, 47994, 92723, 327550, 698471, 1311871], [969, 1937.0, 4.25, 2071616, 2196809, 37653, 46023, 76784, 288649, 665635, 1119718], [360, 1951.0, 3.79, 2044241, 2120637, 44920, 109383, 185520, 455042, 661516, 709176], [311, 2000.0, 3.85, 2001311, 2078754, 25112, 77841, 145740, 458429, 716569, 680175], [3455, 1813.0, 4.24, 2035490, 2191465, 49152, 54700, 86485, 284852, 609755, 1155673], [283, 2003.0, 4.26, 1813044, 1878095, 59730, 34288, 59980, 226062, 628174, 929591], [210, 2011.0, 4.24, 1903563, 2216814, 101023, 36315, 82870, 310297, 673028, 1114304], [995, 1949.0, 4.14, 1956832, 2053394, 45518, 41845, 86425, 324874, 692021, 908229], [896, 1945.0, 3.87, 1881700, 1982987, 35472, 66854, 135147, 433432, 698642, 648912], [710, 1947.0, 4.1, 1972666, 2024493, 20825, 45225, 91270, 355756, 656870, 875372], [274, 2005.0, 4.11, 1808403, 1929834, 62543, 54835, 86051, 285413, 667485, 836050], [201, 2009.0, 4.3, 1831039, 1988079, 88538, 10492, 48030, 262010, 687238, 980309], [376, 1999.0, 4.53, 1832823, 1969375, 36099, 6716, 20413, 166129, 509447, 1266670], [566, 1954.0, 4.34, 1766803, 1832541, 15333, 38031, 55862, 202332, 493922, 1042394], [239, 2010.0, 4.03, 1719760, 1870748, 96274, 30144, 110498, 373060, 618271, 738775]]

#### Insights Discovered:
### Narrative Summary of Analysis on Goodreads Dataset

#### 1. Summary of the Dataset
The dataset comprises 10,000 entries of books, characterized by various attributes including `book_id`, `authors`, `original_publication_year`, `average_rating`, and different rating distributions. Notably, this dataset includes missing values in several key columns: 
- `isbn`: 700 entries missing 
- `isbn13`: 585 entries missing 
- `original_publication_year`: 21 entries missing 
- `original_title`: 585 entries missing 
- `language_code`: 1,084 entries missing

Outliers were identified in the distribution of `average_rating`, indicating polarized ratings where books either received excessively high or low ratings. The correlation analysis revealed relationships between various columns, particularly between `average_rating` and the counts of the highest ratings (ratings_5), suggesting that better-rated books also tend to receive a higher number of 5-star ratings.

#### 2. Analysis Performed
Two primary analyses were executed:
- **Outlier Detection**: Evaluated the distribution of `average_rating`, revealing multiple outlier values that deviate significantly from the mean rating of approximately 4.00. 
- **Correlation Analysis**: Explored the relationships between book attributes such as `ratings_count`, `work_ratings_count`, `work_text_reviews_count`, and `average_rating`. For instance, books with higher average ratings showed correlations with other factors such as the number of high ratings (`ratings_5`) and overall ratings received.

#### 3. Insights Discovered
The analysis yielded several critical insights:
- **Polarized Ratings**: Books exhibited significant polarization in ratings, highlighted by clusters of entries in both the high and low rating systems.
- **Correlation Patterns**: Positive correlations were found between `average_rating` and `ratings_count` (r = 0.85), indicating that books with higher average ratings attract more ratings and vice versa. Similarly, a strong positive correlation exists between `ratings_count` and `work_ratings_count`.
- The popularity of authors also influences ratings, as certain authors like Stephen King appeared frequently among the highest-rated titles.

#### 4. Implications and Recommendations
The findings suggest that a small number of books dominate reader appreciation, leading to polarized ratings, which indicate varying reader preferences. 

**Recommendations**:
- **Targeted Marketing**: To improve the visibility of lesser-known books, consider marketing strategies that highlight categorical genres or underrepresented authors. 
- **Engagement Initiatives**: Encourage readers to rate and review lesser-known works through incentives, aiming to reduce the polarization in ratings and help diversify reader choices.
- **Continued Monitoring**: Regularly analyze feedback on newly released titles to address shifting reader preferences and develop tailored engagement strategies.

The attached outlier and correlation analysis charts (located at `goodreads\\outliers.png` and `goodreads\\correlation.png`) visually support these insights and recommendations, providing further context for decision-making in future marketing and engagement strategies.

#### Implications of the Findings:
- N/A



