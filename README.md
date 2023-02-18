# Sunfresh Network

An all-in-one solution for Sunfresh, an affiliate marketing business ran by a client of mine. The backbone of this project is a Python Flask API backend integrated with a minimal database controller using TinyDB, interfacing an [affiliate marketing Shopify plugin](https://www.secomapp.com/shopify-affiliate-marketing-app/) by [SecomApp](https://www.secomapp.com/). Also includes a minimal Bootstrap + jQuery frontend to rebuild the network and recalculate referral bonuses for every member in the network.

## Background

Back in 2019, my client who was running an affiliate marketing business approached me with a difficulty he had - his business was growing rapidly but he had trouble scaling. In affiliate marketing, every sale made by each member in the affiliate network will have its revenue split and shared amongst multiple levels of the seller's referrers. My client had been keeping track of every member, referrer, transaction, and the calculations of the shared bonuses manually in Excel spreadsheets. With how quickly new members were being recruited into the network, this method of bookkeeping was becoming increasingly tedious to maintain. At the same time, he wanted to gradually shift his sales online in the form of a webstore. One important requirement of the online webstore was the ability to keep track of the referrals for each sale.

## Tackling the Problem

I set up a Shopify webstore for his products. I also discovered a plugin by [SecomApp](https://www.secomapp.com/) that conveniently integrated features that we need such as a list of members and each member's referrer. The member responsible for each successful order made in the webstore is also kept in track. We have then decided to maintain the 'affiliate network' within the SecomApp plugin itself, since it provides a nice dashboard to add/remove members, csv exports, and REST endpoints. One important feature was missing though: the calculation for the bonus revenue that flows up the chain of referrals for each successful sale. 

For this, I built a custom Python backend to scrape the latest network from the SecomApp dashboard. Selenium was used to automate the authentication step and fetching the complete list of members and a directed acyclic graph of the entire affiliate network can be built from it. With the graph ready, revenue calculation became trivial. For each successful sale, I could just traverse the graph upwards to get ancestor nodes of the member who made the sale. Commission is then calculated and updated respectively. As a result, the updated graph now contains the total commission for each member and can be exported to an Excel sheet.
