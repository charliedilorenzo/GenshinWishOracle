# Genshin Wish Oracle

## Index

- [What is this project?](/README.md#what-is-this-project?)
- [How does it work?](/README.md#how-does-it-work?)
- [Existing Errors](/README.md#existing-errors)
- [Informing Data](/README.md#informing-data)

## What is this project?

If you have ever asked youself "I wonder if this many primos is enough to get Baizhu, my favorite character", then this tool was produced in the hopes of accurately answering that question.

Multiple functions are implemented (or to be implemented):

- Wish Simulator: Relatively simple and gives one possible simulation of how a wishing session might go with as accurate statistics as I can provide
- Wish Projection: Using [data from past patchs](/README.md#patch-primo-income), I try to as conservatively as possible estimate the amount of (equivalent) primogems one can get with Welkin and BP as addtional income sources
- Wish Statistics Analysis: Prior I had another project [GenshinWishStats](https://github.com/charliedilorenzo/GenshinWishStats), which derived statistics via brute force repeated simulations. Recently, I've realized how to analytically derive the statistics for Genshin Impact wishing including pity, guaranteed, fate points, etc. I also have crossed-check this method with the other one and they agree with great accuracy (though the brute force method has variance so there is always some difference).
- Custom Banners: Store different banners to be used in the simulator or statistics analyzer

## How does it work?

&ensp;&ensp; The analytical functions works recursively and use the solution for connecting wish number/pity level/guaranteed state/fate point combinations in order to derive subsequent solutions. While the previous process took around 24 hours to calculate solutions for a given pity/guaranteed combination on character banner for all amounts of wishes, now it takes around 2 minutes to calculate for all wish numbers, all pity, all guaranteed, and all fate points.

## Existing Errors

&ensp;&ensp; The major point of error would be that the soft pity region (around with 74-90 for character banner) is likely not fully accurately given. That is why I will allow people to override my defaults and give whatever values they desire for pity distribution. Once I have progressed the project further in functionality I will scour the internet to find more accurate numbers. However, as the case may be the function will work properly ASSUMING that eventually I get more accurate pity distribution.

## Informing Data

### paimon.moe

&ensp;&ensp; [paimon.moe](https://paimon.moe/wish/tally) is great for all sorts of things and I highly recommend it. First I want to use the caveats that exist with me using it for data :

- initial pity level might not be uniform or predictable across banners
- pity level might not be accurately represented since wish data can expire for in game storage (this happened to me)
- pity level might not be accurately represented if the probabilities don't represent what I think
- people may accidentally mess up with automatic input
- people may accidentally mess up with manual input
- people can input false data to the database if they want
- etc

As I said I love this side it performs pretty much all of its functions very well. I use it to:

- store my wish data - with the Wish Counter
- make sure that I have enough materials for a character - with the Calculator
- keep track of which characters I am building - with the Todo List
- keep track of my achievements (this one I use a *TON*) - with the Database/Achievements

### Patch Primo Income

&ensp;&ensp; I use [this spreadsheet](https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vQ29M_-mbMbNgJl5c1ZWJwqgd1sFR6NW8A1Wwy85BUHCZHGtKwfrw_Jy68wd1OOyE6h7jQfEbOckjaM/pubhtml) to estimate how many wishes will be given per update. I estimate around 1500 primogems from events per update. This should be undershooting the data from here for all updates.
