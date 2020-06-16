# Trading Algorithms
## Description:
Our trading strategy is split into two distinct algorithms. One is the pairs mean reversion algorithm and the other is a foreign exchange strategy based on the RSI and MACD indicators. Only the pairs algorithm is complete at this time as the forex algo is a work in progress. 
## An Overview of the Pairs Algorithm:
This algo is very simple. We must first design a sub algorithm to calculate equities that are cointegrated (think pepsi vs coke). We then take these two equities and measure their moving averages over two distinct time periods (for example 5 days vs 60 days). By calculating these averages we can track the overall predicted changes in the price of each equity. Then we can map the ratio between the two equities, by doing this we can see when one is either outpreforming or underpreforming compared to the expected ratio between them (i.e. if one stock is massivley outpreforming its corrolated partner or underpreforming compared to its partner). We can then manipulate this to be constantly updating during the trading day (in this case we recalculate a moving average every hour). From this information we can calculate the z score of the pair (to check if one is outpreforming/underpreforming) and trade accordingly. Mean reversion comes into play because if one member of the pair is outpreforming the average we can predict, based on the thesis of mean reversion, that it will return to its expected value. As a result we can short the outpreformer and go long on the underpreformer and generate profit on both sides of the pair. 
### Part 1: Calculating Pairs 
The algorithm to calculate pairs is located in the find_pairs_algo.py file. Basically, we take a set of stocks and get its historical data (using the TD ameritrade api, setup for this api is located in the Analysis_TDA.py file), for the close price over the past year. We then use this close data to calculate the moving average over time for this equity. It is important to note here that we are using the pvalue of each stock (not plotting the raw price data) because this way we can normalize our data to account for variations in stock valuation (ex. tsla stock is more expensive than apple so to compare them effectivley we use the pvalue). 
After we do this for two equities we can generate our first plot:

<img width="632" alt="Screen Shot 2020-05-17 at 7 17 29 PM" src="https://user-images.githubusercontent.com/65433939/84729738-6edf3880-af62-11ea-939c-bd5683fbe4b8.png">

After this it is not too difficult to plot the ratio between the two equities. We just take the data that represents the price of stock 1 and divide that by the data that represents stock 2. We can also add a mean value which shows the mean value of our pvalue graph overall.
We can also plot this relationship:

![98312711_1099420207120827_8587996518072451072_n](https://user-images.githubusercontent.com/65433939/84730147-6d624000-af63-11ea-9370-7ec2f1e83192.png)

Now that we have calculated a mean value based on all the data in our graph, we can use this mean value to see generally how cointegrated these two equities are. Given this relationship we can create a basic heatmap to map how corrolated stocks are to each other given the mean value. Our heatmap will isolate the most corrolated stocks out of a set. We will use this data to tell our actual algorithm which pairs to trade.

Here is an initial heatmap:

<img width="635" alt="Screen Shot 2020-06-15 at 11 58 50 PM" src="https://user-images.githubusercontent.com/65433939/84730447-317baa80-af64-11ea-8caa-9524b8c31f5b.png">

Here is a heatmap comparing all 500 stocks in the s&p 500.

<img width="631" alt="Screen Shot 2020-05-19 at 6 03 45 PM" src="https://user-images.githubusercontent.com/65433939/84730493-48220180-af64-11ea-9d1b-61fcdaff5589.png">

To inform the actual model we used sector data based on comparing all stocks in sector specific ETFs.

### Part 2: Trading
Now that we have isolated our pairs we can move on to trading. The code for this portion is located in the paper_pairs_algo.py file and the backtesting_pairs_algo.py file. 
Given two stocks we can calculate the moving average of the ratio between them (stock1/stock2) and calculate its z score. This will tell us that if the stock is between 1 and -1 the pair is relativley corrolated and acting as it is expected to. However if the zscore is above one we know that we must sell the ratio by short selling the overpreforming stock and going long on the underpreforming one (vice versa for if the zscore is below -1). This way we can liquidate our positions if they move to between 0.5 and -0.5 in order to gain our profits once they return to expected preformance. 

We can graph this on the ratio with buy and sell signals:

<img width="1497" alt="Screen Shot 2020-05-22 at 12 02 34 AM" src="https://user-images.githubusercontent.com/65433939/84731104-d2b73080-af65-11ea-87d1-fa2553909d2e.png">

Now we can dissociate this to each individual member of the pair:

<img width="1782" alt="Screen Shot 2020-05-22 at 12 03 35 AM" src="https://user-images.githubusercontent.com/65433939/84731116-dba80200-af65-11ea-8580-74101164398d.png">

From here it is very easy to isolate the values at these buy/sell signals and trade accordingly. 

### Final Thoughts:
This algorithm is valuable in that it is profitable no matter the market conditions, even during the recent recession this algorithm is unaffected, because we only trade based on a related pair our profits only change when one member of the pair changes in response to the other, as opposed to changing in response to the market. This makes market events particularly profitable (quarterly earnings, mergers, etc.). There is still room to grow in terms of the statistics side of the algorithm, by using more advanced modeling techniques we could potentially get better predictions. 

To Do:
- There is still much to be done on the forex algorithm and I will update this once that is further along. 
- We still need to optimize the pairs algorithm based on our paper trading results from the past week and a half.
