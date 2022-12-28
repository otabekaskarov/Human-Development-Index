Human Development Index Analysis Application
1. scrapes the most recent HDI score for each country from the Wikipedia
HDI article;
2. gets the data for each country in the HDI list using restcountries API
(find more information on this list on https://restcountries.com/).
3. analyses the correlation between HDI score and countries’
characteristics;
4. saves the analysis result to [current_date].txt file.

The program saves the results to [current_date].txt file and quits. The
.txt report should look something like this:
Correlation report
HDI score
Population 0.435
Area 0.125
Gini 0.658
Neighbours 0.125
