# Sunfresh Network

An all-in-one solution for Sunfresh, an affiliate marketing business ran by a client of mine. The backbone of this project is a Python Flask API backend integrated with a minimal database controller using TinyDB, interfacing an [affiliate marketing Shopify plugin](https://www.secomapp.com/shopify-affiliate-marketing-app/) by [SecomApp](https://www.secomapp.com/). Also includes a minimal Bootstrap + jQuery frontend for the admin running the network to rebuild the network and recalculate referral bonuses for every member in the network.

## Background

Back in 2019, my client who was running an affiliate marketing business approached me with a difficulty he had - his business was growing rapidly but he had trouble scaling. In affiliate marketing, every sale made by each member in the affiliate network will have its revenue split and shared amongst multiple levels of the seller's referrers. My client had been keeping track of every member, referrers, transactions and the calculations of the shared bonuses manually in an Excel Spreadsheet. With how quickly new members are being recruited into the network, this method of bookkeeping is becoming increasingly tedious to maintain. At the same time, he wanted to move some of his sales online in the form of an online shop. One important requirement of the online shop is the ability to keep track of the referrals for each sale.

## Tackling the Problem

I set up a Shopify webstore for him. I also discovered a plugin by [SecomApp](https://www.secomapp.com/) that conveniently integrate features that we need such as keeping track of each member's referrer, and the referrer for each order made within the webstore. We have then decided to maintain the 'affiliate network' within the SecomApp plugin itself, as it has features like a user-friendly dashboard to add/remove members, csv exports, and REST endpoints. One important feature was missing though: the calculation for the distributed revenue for each successful sale as it goes up each level in the chain of referrals. Furthermore, the revenue distribution for each level follows a certain scaling. 

For this, I built a custom Python backend to scrape the latest network from the SecomApp plugin, 
