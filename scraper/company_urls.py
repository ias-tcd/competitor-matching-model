companies_to_urls: dict[str, list[str]] = {
    "adidas": [
        # "https://www.adidas.ie/men-t_shirts",
        # "https://www.adidas.ie/men-black-shoes",
        # "https://www.adidas.ie/men-hoodies",
        # "https://www.adidas.ie/logo_print",
        # "https://www.adidas.ie/logo_print?start=48",
        # "https://www.pinterest.ie/search/pins/?q=adidas&rs=typed",
        # "https://www.pinterest.ie/adidas/adidas-originals/",
        # "https://www.pinterest.ie/search/pins/?q=adidas%20streetwear&rs=typed",
        # "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*FLLKW10QWJCJ_guRKR4olA.jpeg",
        # "https://wallpapercave.com/wp/wp4620709.jpg",
        # "https://wallpapercave.com/wp/wp4620710.jpg",
        # "https://wallpapercave.com/wp/wp4620711.jpg",
        # "https://wallpapercave.com/wp/wp4620713.jpg",
        # "https://wallpapercave.com/wp/wp4620714.jpg",
        # "https://wallpapercave.com/wp/wp4620715.jpg",
        # "https://wallpapercave.com/wp/wp4620716.jpg",
        # "https://wallpapercave.com/wp/wp4620717.jpg",
        # "https://wallpapercave.com/wp/wp4620718.jpg",
        # "https://wallpapercave.com/wp/wp4620719.jpg",
        # "https://wallpapercave.com/wp/wp4592160.jpg",
        # "https://wallpapercave.com/wp/wp2686359.jpg",
        # "https://wallpapercave.com/wp/wp4620723.jpg",
        # "https://wallpapercave.com/wp/wp4620724.jpg",
        # "https://wallpapercave.com/wp/wp4620725.jpg",
        # "https://wallpapercave.com/wp/wp4620726.jpg",
        # "https://wallpapercave.com/wp/wp4620737.jpg",
        # "https://wallpapercave.com/wp/wp4324758.jpg",
        # "https://wallpapercave.com/wp/wp4620739.jpg",
        # "https://wallpapercave.com/wp/wp4620740.jpg",
        # "https://wallpapercave.com/wp/wp4620747.jpg",
        # "https://wallpapercave.com/wp/wp4620748.jpg",
        # "https://wallpapercave.com/wp/wp4620749.jpg",
        # "https://wallpapercave.com/wp/wp4620750.jpg",
        # "https://wallpapercave.com/wp/wp4620751.jpg",
        # "https://wallpapercave.com/wp/wp4620752.jpg",
        # "https://wallpapercave.com/wp/wp4620753.jpg",
        # "https://wallpapercave.com/wp/wp4324990.jpg",
        # "https://wallpapercave.com/wp/wp4620761.jpg",
        # "https://wallpapercave.com/wp/wp2754627.jpg",
        # "https://wallpapercave.com/wp/wp4620764.jpg",
        # "https://wallpapercave.com/wp/wp4620766.jpg",
        # "https://wallpapercave.com/wp/wp4620768.jpg",
        # "https://wallpapercave.com/wp/wp4620773.jpg",
        # "https://wallpapercave.com/wp/wp4620777.jpg",
        # "https://wallpapercave.com/wp/wp4620820.jpg",
        # "https://wallpapercave.com/wp/wp4620821.jpg",
        # "https://wallpapercave.com/wp/wp4620823.jpg",
        # "https://wallpapercave.com/wp/wp4620824.jpg",
        # "https://wallpapercave.com/wp/wp4620825.jpg",
        # "https://wallpapercave.com/wp/wp4620826.jpg",
        # "https://wallpapercave.com/wp/wp4620827.jpg",
        # "https://wallpapercave.com/wp/wp4620828.jpg",
        # "https://wallpapercave.com/wp/wp4620836.jpg",
        # "https://wallpapercave.com/wp/wp4620840.jpg",
        # "https://www.pinterest.ie/adidas/styling-sports-jerseys/",
        # "https://www.adidas.ie/logo_print?start=96",
        # "https://www.pinterest.ie/adidas/festival-style/",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=96",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=144",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=192",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=240",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=288",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=336",
        # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=384",
    ],
    "nike": [
        # "https://www.nike.com/ie/men",
        # "https://www.nike.com/ie/women",
        # "https://www.pinterest.ie/search/pins/?q=nike&rs=typed",
        # "https://ie.pinterest.com/ideas/nike-logo-wallpapers/946319450579/",
        # "https://www.template.net/design-templates/logo/inspiring-nike-logo/",
        # "https://ie.pinterest.com/nike/nike-summer-2021-lookbook/",
        # "https://ie.pinterest.com/nike/nike-m/",
        # "https://ie.pinterest.com/nike/nike-spring-2021-lookbook/",
        # "https://ie.pinterest.com/ideas/nike-men/915704573050/",
        # "https://www.nike.com/ie/w/new-3n82y",
        # "https://www.nike.com/ie/w/best-training-gym-58jtoz76m50",
        # "https://www.nike.com/ie/w/best-jordan-shoes-37eefz76m50zy7ok",
        # "https://www.nike.com/ie/w/best-76m50",
        # "https://www.nike.com/ie/w/lifestyle-accessories-equipment-13jrmzawwpw",
        # "https://www.nike.com/ie/w/older-kids-agibjzv4dh",
        # "https://www.nike.com/ie/w/little-kids-6dacezv4dh",
        # "https://www.nike.com/ie/w/baby-toddlers-kids-2j488zv4dh",
        # "https://www.nike.com/ie/w/mens-sale-clothing-3yaepz6ymx6znik1",
        # "https://www.nike.com/ie/w/womens-sale-clothing-3yaepz5e1x6z6ymx6",
        # "https://www.nike.com/ie/launch?s=upcoming2",
        # "https://www.nike.com/ie/w/member-access-4lbty",
    ],
    # "reebok": [
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=1"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=2"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=3"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=4"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=5"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=6"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=7"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=8"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=9"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=10"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=11"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=12"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/men?categories=147590%7C147555&contextfilters=categories%3A147554&pageindex=13"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/women?categories=147611%7C147649&contextfilters=categories%3A147610&pageindex=1"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/women?categories=147611%7C147649&contextfilters=categories%3A147610&pageindex=3"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/women?categories=147611%7C147649&contextfilters=categories%3A147610&pageindex=6"
    # ),
    # (
    #     "https://www.reebok.eu"
    #     "/en-ie/shopping/women?categories=147611%7C147649&contextfilters=categories%3A147610&pageindex=7"
    # ),
    # ]
    # "north_face": [
    # "https://www.thenorthface.ie/shop/en-gb/tnf-ie/men-men-new-arrivals#banner=Fall23.NewArrivals.img.MLPStockFiller1",
    # "https://www.thenorthface.ie/shop/en-gb/tnf-ie/men-activities-ski-and-snowboard#banner=Fall23.MenSnowsports.img.MLPStockFiller2",
    # "https://www.thenorthface.ie/shop/en-gb/tnf-ie/men-activities-trail-running#banner=Fall23.ActivitiesRunning.img.MLPStockFiller3",
    # "https://www.thenorthface.ie/shop/en-gb/tnf-ie/women-women-new-arrivals#banner=Fall23.NewSeason.img.WLPStockFiller1",
    # "https://www.thenorthface.ie/shop/en-gb/tnf-ie/women-activities-ski-snowboard#banner=Fall23.SnowSports.img.WLPStockFiller2",
    # "https://www.thenorthface.ie/shop/en-gb/tnf-ie/women-activities-trail-running#banner=Fall23.NewRunning.img.WLPStockFiller3",
    # ]
    # "under_armour": [
    # "https://www.underarmour.ie/en-ie/c/mens/?start=0&sz=250",
    # "https://www.underarmour.ie/en-ie/c/boys/shoes/?start=0&sz=120",
    # "https://www.underarmour.ie/en-ie/c/womens/?start=0&sz=120",
    # "https://www.underarmour.ie/en-ie/c/kids/sports/basketball/",
    # "https://www.underarmour.ie/en-ie/c/girls/accessories/?start=0&sz=19",
    # "https://www.underarmour.ie/en-ie/c/outlet/mens-accessories/?start=0&sz=22",
    # "https://www.underarmour.ie/en-ie/c/womens/accessories/?start=1&sz=120",
    # ]
    # "adidas": [
    # "https://www.adidas.ie/men-t_shirts",
    # "https://www.adidas.ie/men-black-shoes",
    # "https://www.adidas.ie/men-hoodies",
    # "https://www.adidas.ie/logo_print",
    # "https://www.adidas.ie/logo_print?start=48",
    # "https://www.pinterest.ie/search/pins/?q=adidas&rs=typed",
    # "https://www.pinterest.ie/adidas/adidas-originals/",
    # "https://www.pinterest.ie/search/pins/?q=adidas%20streetwear&rs=typed",
    # "https://miro.medium.com/v2/resize:fit:1100/format:webp/1*FLLKW10QWJCJ_guRKR4olA.jpeg",
    # "https://wallpapercave.com/wp/wp4620709.jpg",
    # "https://wallpapercave.com/wp/wp4620710.jpg",
    # "https://wallpapercave.com/wp/wp4620711.jpg",
    # "https://wallpapercave.com/wp/wp4620713.jpg",
    # "https://wallpapercave.com/wp/wp4620714.jpg",
    # "https://wallpapercave.com/wp/wp4620715.jpg",
    # "https://wallpapercave.com/wp/wp4620716.jpg",
    # "https://wallpapercave.com/wp/wp4620717.jpg",
    # "https://wallpapercave.com/wp/wp4620718.jpg",
    # "https://wallpapercave.com/wp/wp4620719.jpg",
    # "https://wallpapercave.com/wp/wp4592160.jpg",
    # "https://wallpapercave.com/wp/wp2686359.jpg",
    # "https://wallpapercave.com/wp/wp4620723.jpg",
    # "https://wallpapercave.com/wp/wp4620724.jpg",
    # "https://wallpapercave.com/wp/wp4620725.jpg",
    # "https://wallpapercave.com/wp/wp4620726.jpg",
    # "https://wallpapercave.com/wp/wp4620737.jpg",
    # "https://wallpapercave.com/wp/wp4324758.jpg",
    # "https://wallpapercave.com/wp/wp4620739.jpg",
    # "https://wallpapercave.com/wp/wp4620740.jpg",
    # "https://wallpapercave.com/wp/wp4620747.jpg",
    # "https://wallpapercave.com/wp/wp4620748.jpg",
    # "https://wallpapercave.com/wp/wp4620749.jpg",
    # "https://wallpapercave.com/wp/wp4620750.jpg",
    # "https://wallpapercave.com/wp/wp4620751.jpg",
    # "https://wallpapercave.com/wp/wp4620752.jpg",
    # "https://wallpapercave.com/wp/wp4620753.jpg",
    # "https://wallpapercave.com/wp/wp4324990.jpg",
    # "https://wallpapercave.com/wp/wp4620761.jpg",
    # "https://wallpapercave.com/wp/wp2754627.jpg",
    # "https://wallpapercave.com/wp/wp4620764.jpg",
    # "https://wallpapercave.com/wp/wp4620766.jpg",
    # "https://wallpapercave.com/wp/wp4620768.jpg",
    # "https://wallpapercave.com/wp/wp4620773.jpg",
    # "https://wallpapercave.com/wp/wp4620777.jpg",
    # "https://wallpapercave.com/wp/wp4620820.jpg",
    # "https://wallpapercave.com/wp/wp4620821.jpg",
    # "https://wallpapercave.com/wp/wp4620823.jpg",
    # "https://wallpapercave.com/wp/wp4620824.jpg",
    # "https://wallpapercave.com/wp/wp4620825.jpg",
    # "https://wallpapercave.com/wp/wp4620826.jpg",
    # "https://wallpapercave.com/wp/wp4620827.jpg",
    # "https://wallpapercave.com/wp/wp4620828.jpg",
    # "https://wallpapercave.com/wp/wp4620836.jpg",
    # "https://wallpapercave.com/wp/wp4620840.jpg",
    # "https://www.pinterest.ie/adidas/styling-sports-jerseys/",
    # "https://www.adidas.ie/logo_print?start=96",
    # "https://www.pinterest.ie/adidas/festival-style/",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=96",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=144",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=192",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=240",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=288",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=336",
    # "https://www.adidas.ie/accessories%7Cclothing-logo_print?start=384",
    # ]
}
