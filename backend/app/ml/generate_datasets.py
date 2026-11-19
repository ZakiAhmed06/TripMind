"""
Dataset Generator & Preprocessor for TripMind
Generates 300+ Indian Destinations, 800+ Attractions, Expense Records, Crowd Data, and RAG Knowledge Docs.
"""
import os
import csv
import json
import random
import pandas as pd
import numpy as np

DESTINATIONS_DATA = [
    # North India - Mountains & Heritage
    ("Manali", "Himachal Pradesh", "Mountains", 2800, 12.0, 9.0, 9.5, 6.0, 5.0, 9.2, True, "October - June", 9.4, 32.2396, 77.1887, "High-altitude Himalayan resort town known for snow-capped peaks, Solang Valley adventures, and Old Manali cafes.", "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"),
    ("Shimla", "Himachal Pradesh", "Mountains", 3000, 14.5, 6.5, 8.5, 5.5, 8.0, 8.0, True, "March - June", 9.1, 31.1048, 77.1734, "Colonial-era summer capital of British India with the historic Ridge, Mall Road, and toy train railway.", "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80"),
    ("Dharamshala", "Himachal Pradesh", "Mountains", 2400, 16.0, 7.5, 9.0, 5.0, 8.5, 8.8, True, "September - June", 8.8, 32.2190, 76.3234, "Seat of the Dalai Lama, surrounded by cedar forests on the edge of the Himalayas with vibrant Tibetan culture.", "https://images.unsplash.com/photo-1591871937573-74dbba515c4c?auto=format&fit=crop&w=800&q=80"),
    ("Kasol", "Himachal Pradesh", "Adventure", 2000, 15.0, 9.2, 9.6, 7.5, 4.0, 9.0, False, "March - June", 8.9, 32.0100, 77.3150, "Scenic hamlet in Parvati Valley popular among backpackers, trekkers to Kheerganga, and riverside camping.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),
    ("Spiti Valley", "Himachal Pradesh", "Adventure", 3200, 5.0, 9.8, 9.8, 2.0, 8.0, 9.9, False, "June - September", 9.2, 32.2461, 78.0349, "Cold desert mountain valley famous for ancient Buddhist monasteries, Chandratal lake, and high mountain passes.", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80"),
    ("Dalhousie", "Himachal Pradesh", "Nature", 2600, 14.0, 6.0, 8.8, 4.0, 7.5, 8.2, True, "March - June", 8.3, 32.5387, 75.9710, "Quiet colonial hill retreat with pine-clad valleys, Khajjiar meadows (Mini Switzerland of India), and colonial churches.", "https://images.unsplash.com/photo-1605649487212-47bdab064df8?auto=format&fit=crop&w=800&q=80"),
    ("Bir Billing", "Himachal Pradesh", "Adventure", 2700, 16.5, 9.8, 8.5, 5.0, 6.0, 8.8, True, "September - November", 8.7, 32.0519, 76.7176, "Paragliding capital of India with scenic take-off points, Tibetan monasteries, and tea gardens.", "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"),
    ("Kullu", "Himachal Pradesh", "Nature", 2500, 15.5, 8.5, 9.0, 4.5, 7.0, 8.5, True, "March - June", 8.4, 31.9579, 77.1095, "Valley of Gods, famous for river rafting in the Beas river, apple orchards, and grand Dussehra celebrations.", "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"),
    ("Jibhi", "Himachal Pradesh", "Nature", 2200, 13.0, 8.0, 9.5, 4.0, 5.0, 9.0, True, "March - November", 8.6, 31.6370, 77.3488, "Unexplored paradise in Tirthan Valley featuring pine woods, freshwater streams, and traditional wooden cottages.", "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80"),
    ("Kaza", "Himachal Pradesh", "Adventure", 3100, 4.0, 9.5, 9.2, 2.0, 8.5, 9.6, False, "May - October", 8.7, 32.2276, 78.0710, "Commercial hub of Spiti Valley, home to Key Monastery and the world's highest post office at Hikkim.", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80"),

    # Uttarakhand
    ("Rishikesh", "Uttarakhand", "Adventure", 2100, 22.0, 9.5, 8.5, 5.5, 9.0, 8.5, True, "September - May", 9.5, 30.0869, 78.2676, "Yoga capital of the world on the banks of the sacred Ganges, premier spot for river rafting and bungee jumping.", "https://images.unsplash.com/photo-1596701062351-8c2c14d1fdd1?auto=format&fit=crop&w=800&q=80"),
    ("Nainital", "Uttarakhand", "Nature", 2700, 15.0, 6.0, 9.0, 5.0, 6.5, 8.6, True, "March - June", 9.0, 29.3919, 79.4542, "Charming lake city set around emerald Naini Lake, surrounded by seven verdant hills.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Mussoorie", "Uttarakhand", "Mountains", 2900, 16.0, 6.5, 8.5, 5.5, 7.0, 8.4, True, "March - June", 9.0, 30.4598, 78.0644, "Queen of the Hills, overlooking the Doon Valley and Shivalik ranges with Gun Hill and Kempty Falls.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),
    ("Auli", "Uttarakhand", "Adventure", 3800, 8.0, 9.8, 9.6, 3.0, 4.0, 9.7, True, "December - March", 9.2, 30.5312, 79.5684, "India's premier ski resort with panoramic views of Nanda Devi, world-class slopes, and the highest cable car.", "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80"),
    ("Jim Corbett", "Uttarakhand", "Wildlife", 3500, 24.0, 8.5, 9.5, 3.5, 5.0, 9.2, True, "November - June", 9.1, 29.5300, 78.7747, "India's oldest national park, sanctuary for the majestic Bengal Tiger and wild Asiatic elephants.", "https://images.unsplash.com/photo-1549366021-9f761d450615?auto=format&fit=crop&w=800&q=80"),
    ("Haridwar", "Uttarakhand", "Spiritual", 1800, 24.0, 3.0, 6.5, 2.0, 9.8, 7.5, True, "October - March", 9.2, 29.9457, 78.1642, "Ancient pilgrimage city where the Ganges leaves the Himalayas; world-famous for the evening Ganga Aarti at Har Ki Pauri.", "https://images.unsplash.com/photo-1596701062351-8c2c14d1fdd1?auto=format&fit=crop&w=800&q=80"),
    ("Kedarnath", "Uttarakhand", "Spiritual", 3200, 4.0, 9.0, 9.2, 1.0, 10.0, 9.4, False, "May - October", 9.6, 30.7352, 79.0669, "Revered Jyotirlinga temple standing at 3,583m amidst snow-capped peaks of the Garhwal Himalayas.", "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"),
    ("Badrinath", "Uttarakhand", "Spiritual", 3100, 6.0, 7.5, 9.0, 1.0, 9.9, 9.1, True, "May - October", 9.4, 30.7433, 79.4938, "Holiest of the Char Dham shrines dedicated to Lord Vishnu, set between Nar and Narayana mountain ranges.", "https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=800&q=80"),
    ("Chopta", "Uttarakhand", "Adventure", 2300, 10.0, 9.2, 9.8, 2.0, 7.5, 9.5, True, "April - November", 8.8, 30.4855, 79.1830, "The 'Mini Switzerland of Uttarakhand', base for the trek to Tungnath (highest Shiva temple) and Chandrashila.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),
    ("Valley of Flowers", "Uttarakhand", "Nature", 3400, 12.0, 9.0, 10.0, 1.0, 6.0, 9.9, False, "July - September", 9.3, 30.7280, 79.6053, "UNESCO World Heritage alpine valley blanketed in hundreds of species of blooming wild flowers.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),

    # Jammu & Kashmir and Ladakh
    ("Srinagar", "Jammu and Kashmir", "Nature", 3200, 13.0, 6.0, 9.8, 5.0, 8.5, 9.7, True, "April - October", 9.6, 34.0837, 74.7973, "Heaven on Earth featuring serene Dal Lake houseboats, Mughal gardens, and shikara rides.", "https://images.unsplash.com/photo-1598091383021-15ddea10925d?auto=format&fit=crop&w=800&q=80"),
    ("Gulmarg", "Jammu and Kashmir", "Adventure", 4200, 7.0, 9.8, 9.6, 4.0, 5.0, 9.8, True, "December - March", 9.5, 34.0484, 74.3805, "Meadow of flowers boasting the world's second-highest operating cable car (Gondola) and premier skiing slopes.", "https://images.unsplash.com/photo-1548013146-72479768bada?auto=format&fit=crop&w=800&q=80"),
    ("Pahalgam", "Jammu and Kashmir", "Nature", 3500, 10.0, 8.0, 9.8, 3.5, 6.0, 9.6, True, "April - September", 9.3, 34.0161, 75.1950, "Valley of Shepherds surrounded by pine forests, Lidder river trout fishing, and Betaab Valley views.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Leh", "Ladakh", "Adventure", 3600, 6.0, 9.7, 9.5, 4.5, 9.0, 9.9, False, "May - September", 9.6, 34.1526, 77.5771, "High-altitude desert wonderland of Tibetan gompas, dramatic moonscapes, and vibrant bazaars.", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80"),
    ("Nubra Valley", "Ladakh", "Adventure", 3800, 8.0, 9.5, 9.7, 2.0, 7.5, 9.8, False, "June - September", 9.3, 34.6863, 77.5673, "Valley of flowers with double-humped Bactrian camels, sand dunes at Hunder, and Diskit Monastery.", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80"),
    ("Pangong Lake", "Ladakh", "Photography", 3900, 4.0, 8.5, 10.0, 1.0, 3.0, 10.0, False, "May - September", 9.7, 33.7595, 78.6674, "Famous endorheic lake stretching from India to China that changes color from azure to turquoise to deep navy.", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80"),

    # Rajasthan
    ("Jaipur", "Rajasthan", "Heritage", 2800, 26.0, 5.0, 6.0, 7.0, 9.9, 9.2, True, "October - March", 9.6, 26.9124, 75.7873, "The Pink City of Amber Fort, Hawa Mahal, City Palace, bustling spice bazaars, and rich Rajputana heritage.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Udaipur", "Rajasthan", "Heritage", 3400, 25.0, 5.5, 8.5, 7.5, 9.8, 9.8, True, "September - March", 9.7, 24.5854, 73.7125, "City of Lakes and Venice of the East, famous for Lake Pichola, floating palaces, and romantic sunset boat cruises.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Jodhpur", "Rajasthan", "Heritage", 2600, 27.0, 6.5, 5.5, 6.0, 9.7, 9.4, True, "October - March", 9.2, 26.2389, 73.0243, "The Blue City crowned by the towering Mehrangarh Fort, Umaid Bhawan Palace, and desert traditions.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Jaisalmer", "Rajasthan", "Culture", 3100, 27.5, 8.5, 7.0, 6.0, 9.6, 9.7, True, "October - March", 9.4, 26.9157, 70.9083, "The Golden City of Thar Desert with a living sandstone fort, golden sand dune safaris, and folk dance camps.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Pushkar", "Rajasthan", "Spiritual", 2000, 26.0, 5.0, 6.5, 5.0, 9.2, 8.9, True, "October - March", 8.8, 26.4897, 74.5511, "Holy lake town housing one of the world's few Lord Brahma temples and the iconic annual Pushkar Camel Fair.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Ranthambore", "Rajasthan", "Wildlife", 3600, 26.5, 8.2, 9.0, 3.0, 8.0, 9.3, True, "October - April", 9.3, 26.0173, 76.5026, "Renowned national park where Royal Bengal Tigers roam amidst the ruins of a 10th-century jungle fortress.", "https://images.unsplash.com/photo-1549366021-9f761d450615?auto=format&fit=crop&w=800&q=80"),
    ("Mount Abu", "Rajasthan", "Mountains", 2800, 20.0, 6.0, 8.0, 4.5, 8.5, 8.2, True, "Year-round", 8.5, 24.5926, 72.7156, "Rajasthan's only hill station featuring the intricately carved marble Dilwara Jain temples and Nakki Lake.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),

    # Goa & Coastal West
    ("North Goa", "Goa", "Nightlife", 3500, 28.0, 8.5, 8.0, 10.0, 7.0, 8.8, True, "November - February", 9.8, 15.5494, 73.7535, "Vibrant beach enclave famous for Baga & Anjuna beaches, beach shacks, vibrant clubs, water sports, and Saturday night markets.", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80"),
    ("South Goa", "Goa", "Beaches", 3800, 28.0, 6.5, 9.2, 6.5, 8.0, 9.2, True, "November - March", 9.5, 15.2832, 73.9862, "Serene white sand shores of Palolem and Agonda, Portuguese colonial mansions, and luxury beachfront resorts.", "https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=800&q=80"),
    ("Gokarna", "Karnataka", "Beaches", 2200, 27.5, 7.8, 9.0, 6.0, 8.2, 9.1, True, "October - March", 9.0, 14.5479, 74.3188, "Laidback coastal temple town with crescent-shaped Om Beach, Kudle Beach, and cliffside trekking.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"),
    ("Alibaug", "Maharashtra", "Beaches", 2800, 27.0, 6.0, 7.8, 6.0, 7.2, 8.0, True, "November - March", 8.4, 18.6414, 72.8722, "Coastal weekend getaway near Mumbai known for Kolaba Sea Fort, black sand beaches, and fresh seafood.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"),
    ("Tarkarli", "Maharashtra", "Adventure", 2600, 28.0, 9.2, 8.8, 4.0, 7.0, 8.6, True, "October - March", 8.5, 16.0381, 73.4862, "Konkan coastline gem celebrated for clear waters, scuba diving, coral reefs, and Malvani cuisine.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"),

    # Kerala - God's Own Country
    ("Munnar", "Kerala", "Nature", 2800, 18.0, 7.0, 9.8, 3.5, 5.0, 9.5, True, "September - March", 9.6, 10.0889, 77.0595, "Rolling tea plantations, misty green peaks, cascading Cheeyappara falls, and rare Neelakurinji blooms.", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80"),
    ("Alleppey", "Kerala", "Nature", 3400, 28.0, 5.0, 9.5, 4.0, 6.0, 9.6, True, "October - February", 9.6, 9.4981, 76.3388, "Venice of the East, world-famous for overnight traditional houseboat cruises across palm-fringed backwaters.", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80"),
    ("Wayanad", "Kerala", "Nature", 2700, 21.0, 8.0, 9.6, 4.0, 6.5, 9.1, True, "October - May", 9.1, 11.6854, 76.1320, "Lush forested district of spice plantations, prehistoric Edakkal Caves, Chembra Peak heart-shaped lake, and waterfalls.", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80"),
    ("Varkala", "Kerala", "Beaches", 2500, 28.5, 7.5, 9.0, 7.0, 7.0, 9.4, True, "October - March", 9.2, 8.7379, 76.7163, "Dramatic red laterite cliffs bordering the Arabian Sea, cliffside boho cafes, and natural mineral springs.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"),
    ("Kochi", "Kerala", "Culture", 2900, 29.0, 5.5, 7.5, 7.0, 9.5, 8.8, True, "October - April", 9.3, 9.9312, 76.2673, "Historic port city blending Portuguese, Dutch, and British colonial heritage with iconic Chinese fishing nets.", "https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=800&q=80"),
    ("Thekkady", "Kerala", "Wildlife", 2900, 22.0, 7.5, 9.4, 3.5, 5.5, 8.9, True, "September - March", 8.9, 9.6031, 77.1615, "Periyar Tiger Reserve boat safaris, fragrant cardamom plantations, and traditional Kathakali & Kalaripayattu shows.", "https://images.unsplash.com/photo-1549366021-9f761d450615?auto=format&fit=crop&w=800&q=80"),
    ("Kovalam", "Kerala", "Beaches", 3200, 28.0, 6.5, 8.5, 6.5, 6.0, 8.7, True, "November - February", 8.8, 8.4004, 76.9787, "Crescent beaches anchored by the iconic red-and-white striped lighthouse, ayurvedic spas, and catamaran rides.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"),

    # Karnataka & Tamil Nadu
    ("Coorg", "Karnataka", "Nature", 2800, 19.0, 7.2, 9.7, 4.5, 6.5, 9.2, True, "October - April", 9.2, 12.3375, 75.8069, "The Scotland of India, blanketed in aromatic coffee estates, misty hills, Abbey Falls, and Tibetan settlement at Bylakuppe.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Hampi", "Karnataka", "Heritage", 2100, 27.0, 7.0, 7.5, 5.0, 10.0, 9.8, True, "October - February", 9.6, 15.3350, 76.4600, "UNESCO World Heritage ancient ruins of Vijayanagara Empire amidst surreal boulder-strewn landscapes.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Mysore", "Karnataka", "Heritage", 2400, 25.0, 4.5, 7.0, 5.0, 9.7, 8.7, True, "October - March", 9.2, 12.2958, 76.6394, "City of Palaces, famous for the magnificent illuminated Mysore Palace, sandalwood craft, and silk sarees.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Chikmagalur", "Karnataka", "Mountains", 2600, 20.0, 8.0, 9.5, 4.0, 5.0, 9.1, True, "September - March", 8.9, 13.3161, 75.7720, "Coffee capital of Karnataka, home to Mullayanagiri (highest peak in Karnataka) and scenic Baba Budangiri.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),
    ("Ooty", "Tamil Nadu", "Mountains", 2900, 15.0, 6.0, 9.0, 5.0, 7.0, 8.9, True, "March - June", 9.3, 11.4102, 76.6950, "Queen of Nilgiris with the Nilgiri Mountain Toy Train, Botanical Gardens, and sprawling tea estates.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),
    ("Kodaikanal", "Tamil Nadu", "Mountains", 2700, 16.0, 6.5, 9.2, 4.0, 6.0, 9.0, True, "September - May", 9.1, 10.2381, 77.4892, "Princess of Hill Stations set around star-shaped Kodai Lake, Pillar Rocks, and pine forests.", "https://images.unsplash.com/photo-1589182373726-e4f658ab50f0?auto=format&fit=crop&w=800&q=80"),
    ("Pondicherry", "Puducherry", "Culture", 2900, 28.0, 5.5, 7.5, 7.5, 9.0, 9.2, True, "October - March", 9.4, 11.9416, 79.8083, "French colonial quarter with pastel yellow mansions, tree-lined boulevards, Promenade beach, and Auroville.", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"),
    ("Madurai", "Tamil Nadu", "Spiritual", 1900, 29.0, 3.5, 5.5, 4.0, 10.0, 8.6, True, "October - March", 9.1, 9.9252, 78.1198, "Temple City built around the architectural marvel of Meenakshi Amman Temple with towering sculpted gopurams.", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"),
    ("Rameswaram", "Tamil Nadu", "Spiritual", 2200, 28.5, 5.0, 7.0, 3.0, 9.8, 8.8, True, "October - April", 9.0, 9.2876, 79.3129, "Island pilgrimage destination connected by Pamban Bridge, Ramanathaswamy Temple corridors, and Dhanushkodi ghost town.", "https://images.unsplash.com/photo-1582510003544-4d00b7f74220?auto=format&fit=crop&w=800&q=80"),

    # Northeast & East India
    ("Darjeeling", "West Bengal", "Mountains", 2700, 13.0, 7.0, 9.5, 5.0, 8.0, 9.6, True, "March - May & Oct - Dec", 9.5, 27.0410, 88.2663, "Queen of the Hills facing Mount Kanchenjunga, world-renowned Darjeeling tea gardens, and Himalayan toy train.", "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"),
    ("Gangtok", "Sikkim", "Mountains", 2800, 14.0, 8.0, 9.4, 6.0, 8.5, 9.4, True, "September - June", 9.4, 27.3389, 88.6065, "Clean, vibrant capital of Sikkim offering views of Kanchenjunga, Rumtek monastery, and MG Marg strolls.", "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"),
    ("Pelling", "Sikkim", "Nature", 2400, 12.0, 7.5, 9.8, 3.0, 8.0, 9.7, True, "September - May", 8.9, 27.3167, 88.2333, "Quiet hill destination offering closest views of Mount Kanchenjunga, Pemayangtse Monastery, and Skywalk.", "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"),
    ("Shillong", "Meghalaya", "Nature", 2600, 16.0, 7.5, 9.5, 6.5, 7.0, 9.2, True, "September - May", 9.3, 25.5788, 91.8933, "Scotland of the East with pine hills, lively music scene, Umiam Lake, and Elephant Falls.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Cherrapunji", "Meghalaya", "Nature", 2500, 15.0, 8.5, 9.8, 3.0, 6.0, 9.7, True, "October - May", 9.2, 25.2702, 91.7323, "Fabled rainy wonderland famous for ancient living root bridges, Nohkalikai Falls, and limestone caves.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Kaziranga", "Assam", "Wildlife", 3300, 23.0, 8.0, 9.5, 3.0, 5.0, 9.4, True, "November - April", 9.4, 26.5775, 93.1711, "UNESCO World Heritage sanctuary harboring two-thirds of the world's great one-horned rhinoceroses.", "https://images.unsplash.com/photo-1549366021-9f761d450615?auto=format&fit=crop&w=800&q=80"),
    ("Tawang", "Arunachal Pradesh", "Adventure", 3200, 8.0, 9.5, 9.7, 2.0, 9.2, 9.8, False, "March - October", 9.1, 27.5861, 91.8594, "High-altitude Himalayan haven home to the 400-year-old Tawang Monastery and Sela Pass at 13,700 ft.", "https://images.unsplash.com/photo-1581793745862-99fde7fa73d2?auto=format&fit=crop&w=800&q=80"),
    ("Ziro Valley", "Arunachal Pradesh", "Culture", 2300, 15.0, 8.0, 9.6, 5.0, 8.5, 9.5, True, "March - October", 8.8, 27.5950, 93.8385, "Idyllic pine-clad plateau home to the Apatani tribe and the world-renowned outdoor Ziro Music Festival.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Varanasi", "Uttar Pradesh", "Spiritual", 1900, 25.0, 4.0, 6.0, 5.5, 10.0, 9.8, True, "October - March", 9.8, 25.3176, 82.9739, "One of the oldest continuously inhabited cities in the world, iconic Ganga Ghats, and evening Aarti.", "https://images.unsplash.com/photo-1561361513-2d000a50f0dc?auto=format&fit=crop&w=800&q=80"),
    ("Agra", "Uttar Pradesh", "Heritage", 2400, 25.0, 4.0, 5.5, 5.0, 10.0, 9.9, True, "October - March", 9.9, 27.1767, 78.0081, "Home to the Taj Mahal, one of the Seven Wonders of the World, Agra Fort, and Fatehpur Sikri.", "https://images.unsplash.com/photo-1564507592333-c60657eea523?auto=format&fit=crop&w=800&q=80"),
    ("Amritsar", "Punjab", "Spiritual", 2000, 22.0, 4.0, 6.0, 6.0, 9.8, 9.2, True, "October - March", 9.5, 31.6340, 74.8723, "Spiritual center of Sikhism, housing the glistening Golden Temple (Harmandir Sahib) and Wagah Border ceremony.", "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"),
    ("Khajuraho", "Madhya Pradesh", "Heritage", 2200, 25.0, 5.0, 6.5, 3.5, 9.9, 9.4, True, "October - March", 9.1, 24.8318, 79.9199, "UNESCO World Heritage Hindu and Jain temples renowned for exquisite medieval erotic stone sculptures.", "https://images.unsplash.com/photo-1600100397608-f010f443a532?auto=format&fit=crop&w=800&q=80"),
    ("Puri", "Odisha", "Spiritual", 2100, 27.0, 5.5, 7.5, 4.5, 9.5, 8.5, True, "October - March", 9.0, 19.8135, 85.8312, "Holy coastal city renowned for the sacred Jagannath Temple, annual Rath Yatra, and golden beaches.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"),
    ("Havelock Island", "Andaman and Nicobar", "Beaches", 4600, 27.5, 9.0, 9.8, 6.0, 4.0, 9.9, True, "October - May", 9.7, 11.9761, 92.9876, "Tropical island paradise boasting Radhanagar Beach (Asia's best beach), scuba diving, and bioluminescence.", "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80")
]

# Function to synthesize additional destinations systematically to reach 300+ destinations across all regions of India
STATE_REGIONS = {
    "Himachal Pradesh": ["Kullu", "Mandi", "Palampur", "Chamba", "Kinnaur", "Kalpa", "Sangla", "Narkanda", "Solan", "Barot Valley", "Shoja", "Tirthan Valley", "Kaza", "Tabo", "Keylong"],
    "Uttarakhand": ["Lansdowne", "Ranikhet", "Kausani", "Binsar", "Mukteshwar", "Dhanaulti", "Chakrata", "Tehri Garhwal", "Pangot", "Almora", "Munsiyari", "Kanatal", "Uttarkashi", "Chamoli", "Pithoragarh"],
    "Rajasthan": ["Bikaner", "Chittorgarh", "Kumbhalgarh", "Mandawa", "Shekhawati", "Alwar", "Bharatpur", "Bundi", "Sawai Madhopur", "Kota", "Barmer", "Nagaur", "Ranakpur", "Nathdwara"],
    "Maharashtra": ["Lonavala", "Khandala", "Mahabaleshwar", "Panchgani", "Matheran", "Igatpuri", "Bhandardara", "Lavasa", "Kolhapur", "Aurangabad", "Ajanta Ellora", "Nashik", "Ratnagiri", "Sindhudurg", "Ganpatipule", "Murud Janjira", "Kashid", "Chiplun", "Tadoba", "Pench Maharashtra"],
    "Goa": ["Arambol", "Morjim", "Vagator", "Candolim", "Calangute", "Panaji", "Old Goa", "Colva", "Benaulim", "Cavelossim", "Agonda", "Butterfly Beach", "Cabo de Rama", "Dudhsagar", "Divar Island"],
    "Kerala": ["Vagamon", "Ponmudi", "Bekal", "Kannur", "Kozhikode", "Kumarakom", "Marari", "Poovar", "Athirappilly", "Silent Valley", "Nelliyampathy", "Thiruvananthapuram", "Idukki", "Gavi", "Bekal Fort"],
    "Karnataka": ["Dandeli", "Badami", "Aihole", "Pattadakal", "Kabini", "Bandipur", "Nagarhole", "Kudremukh", "Sakleshpur", "Agumbe", "Udupi", "Murudeshwar", "Bijapur", "Belur", "Halebidu", "Jog Falls"],
    "Tamil Nadu": ["Yercaud", "Valparai", "Coonoor", "Yelagiri", "Kanyakumari", "Thanjavur", "Mahabalipuram", "Chettinad", "Tiruvannamalai", "Chidambaram", "Kanchipuram", "Pollachi", "Dhanushkodi"],
    "West Bengal": ["Kalimpong", "Kurseong", "Mirik", "Sundarbans", "Digha", "Mandarmani", "Bakkhali", "Shantiniketan", "Bishnupur", "Dooars", "Jaldapara", "Lava Lolegaon", "Rishop"],
    "Sikkim": ["Lachung", "Lachen", "Yumthang Valley", "Ravangla", "Namchi", "Yuksom", "Zuluk", "Aritar", "Geyzing", "Borong"],
    "Meghalaya": ["Dawki", "Mawlynnong", "Nongriat", "Jowai", "Mawsynram", "Balpakram", "Williamnagar", "Kongthong"],
    "Assam": ["Majuli Island", "Manas National Park", "Guwahati", "Tezpur", "Haflong", "Sivasagar", "Pobitora Wildlife Sanctuary", "Dibrugarh"],
    "Arunachal Pradesh": ["Dirang", "Bomdila", "Mechuka", "Roing", "Pasighat", "Namdapha", "Bhalukpong", "Anini"],
    "Ladakh": ["Kargil", "Zanskar Valley", "Tso Moriri", "Hanle", "Alchi", "Hemis", "Lamayuru", "Turtuk"],
    "Jammu and Kashmir": ["Sonamarg", "Doodhpathri", "Yusmarg", "Aru Valley", "Patnitop", "Bhaderwah", "Gurez Valley", "Verinag"],
    "Madhya Pradesh": ["Pachmarhi", "Bandhavgarh", "Kanha National Park", "Orchha", "Gwalior", "Ujjain", "Mandu", "Bhimbetka", "Bhedaghat", "Sanchi", "Pench MP", "Panna National Park"],
    "Gujarat": ["Rann of Kutch", "Gir National Park", "Dwarka", "Somnath", "Statue of Unity", "Saputara", "Diu", "Mandvi", "Champaner", "Modhera", "Patan"],
    "Odisha": ["Konark", "Bhubaneswar", "Chilika Lake", "Gopalpur", "Simlipal", "Chandipur", "Dhauli", "Raghurajpur"],
    "Andhra Pradesh": ["Araku Valley", "Tirupati", "Visakhapatnam", "Gandikota", "Borra Caves", "Horsley Hills", "Srisailam", "Lepakshi"],
    "Telangana": ["Hyderabad", "Warangal", "Nagarjuna Sagar", "Ananthagiri Hills", "Ramappa Temple"],
    "Uttar Pradesh": ["Lucknow", "Vrindavan", "Mathura", "Ayodhya", "Prayagraj", "Sarnath", "Jhansi", "Dudhwa National Park"],
    "Punjab": ["Anandpur Sahib", "Patiala", "Bathinda", "Kapurthala"],
    "Andaman and Nicobar": ["Neil Island", "Port Blair", "Baratang", "Ross Island", "Diglipur"],
    "Goa & Daman": ["Daman", "Silvassa"]
}

CATEGORY_ATTRIBUTES = {
    "Mountains": {"temp": 14.0, "budget": 2700, "adventure": 8.0, "nature": 9.5, "nightlife": 4.5, "heritage": 6.0, "photo": 9.2},
    "Beaches": {"temp": 28.0, "budget": 3100, "adventure": 7.5, "nature": 8.5, "nightlife": 8.5, "heritage": 5.5, "photo": 9.0},
    "Heritage": {"temp": 26.0, "budget": 2400, "adventure": 4.5, "nature": 5.5, "nightlife": 5.5, "heritage": 9.8, "photo": 9.1},
    "Adventure": {"temp": 16.0, "budget": 3000, "adventure": 9.8, "nature": 9.0, "nightlife": 5.0, "heritage": 5.0, "photo": 9.4},
    "Wildlife": {"temp": 24.0, "budget": 3300, "adventure": 8.2, "nature": 9.7, "nightlife": 3.0, "heritage": 5.0, "photo": 9.3},
    "Spiritual": {"temp": 25.0, "budget": 1800, "adventure": 3.5, "nature": 6.5, "nightlife": 2.5, "heritage": 9.6, "photo": 8.5},
    "Nature": {"temp": 18.0, "budget": 2600, "adventure": 7.0, "nature": 9.8, "nightlife": 3.5, "heritage": 5.5, "photo": 9.5},
    "Culture": {"temp": 25.0, "budget": 2500, "adventure": 5.5, "nature": 7.0, "nightlife": 6.5, "heritage": 9.0, "photo": 9.0},
    "Nightlife": {"temp": 28.0, "budget": 3600, "adventure": 8.0, "nature": 7.5, "nightlife": 9.8, "heritage": 6.0, "photo": 8.7},
    "Food": {"temp": 26.0, "budget": 2300, "adventure": 5.0, "nature": 6.0, "nightlife": 7.5, "heritage": 8.5, "photo": 8.5},
    "Photography": {"temp": 15.0, "budget": 3200, "adventure": 8.5, "nature": 9.8, "nightlife": 3.5, "heritage": 7.5, "photo": 10.0}
}


def build_full_dataset():
    random.seed(42)
    np.random.seed(42)
    records = []
    
    # Add verified destinations first
    dest_id = 1
    existing_names = set()
    
    for item in DESTINATIONS_DATA:
        name, state, cat, budget, temp, adv, nat, nite, her, pho, fam, season, pop, lat, lon, desc, img = item
        records.append({
            "destination_id": dest_id,
            "destination_name": name,
            "state": state,
            "country": "India",
            "category": cat,
            "average_budget": budget,
            "average_temperature": temp,
            "adventure_score": adv,
            "nature_score": nat,
            "nightlife_score": nite,
            "heritage_score": her,
            "photography_score": pho,
            "family_friendly": fam,
            "best_season": season,
            "popularity_score": pop,
            "latitude": lat,
            "longitude": lon,
            "description": desc,
            "image_url": img
        })
        existing_names.add(name)
        dest_id += 1

    # Synthesize additional Indian destinations to reach 320+ high-quality destinations
    cat_keys = list(CATEGORY_ATTRIBUTES.keys())
    state_coords = {
        "Himachal Pradesh": (31.9, 77.1),
        "Uttarakhand": (30.1, 79.0),
        "Rajasthan": (26.5, 74.0),
        "Maharashtra": (18.5, 73.8),
        "Goa": (15.4, 73.8),
        "Kerala": (10.1, 76.5),
        "Karnataka": (13.5, 75.8),
        "Tamil Nadu": (11.0, 78.0),
        "West Bengal": (25.0, 88.0),
        "Sikkim": (27.4, 88.5),
        "Meghalaya": (25.5, 91.5),
        "Assam": (26.2, 92.5),
        "Arunachal Pradesh": (27.8, 93.5),
        "Ladakh": (34.2, 77.6),
        "Jammu and Kashmir": (33.8, 74.9),
        "Madhya Pradesh": (23.2, 77.4),
        "Gujarat": (22.5, 71.5),
        "Odisha": (20.3, 85.8),
        "Andhra Pradesh": (16.5, 80.6),
        "Telangana": (17.4, 78.5),
        "Uttar Pradesh": (26.8, 81.0),
        "Punjab": (31.1, 75.3),
        "Andaman and Nicobar": (11.7, 92.7),
        "Goa & Daman": (20.4, 72.8)
    }

    for state, towns in STATE_REGIONS.items():
        base_lat, base_lon = state_coords.get(state, (22.0, 78.0))
        for town in towns:
            if town in existing_names:
                continue
            
            # Select appropriate category based on state geography
            if state in ["Himachal Pradesh", "Uttarakhand", "Sikkim", "Arunachal Pradesh", "Jammu and Kashmir", "Ladakh"]:
                cat = random.choice(["Mountains", "Adventure", "Nature", "Photography", "Spiritual"])
            elif state in ["Goa", "Andaman and Nicobar"]:
                cat = random.choice(["Beaches", "Nightlife", "Adventure"])
            elif state in ["Rajasthan", "Madhya Pradesh", "Uttar Pradesh"]:
                cat = random.choice(["Heritage", "Culture", "Wildlife", "Spiritual", "Food"])
            elif state in ["Kerala", "Karnataka", "Tamil Nadu"]:
                cat = random.choice(["Nature", "Mountains", "Heritage", "Beaches", "Culture", "Wildlife"])
            else:
                cat = random.choice(cat_keys)

            attr = CATEGORY_ATTRIBUTES[cat]
            jitter_lat = base_lat + round(random.uniform(-0.8, 0.8), 4)
            jitter_lon = base_lon + round(random.uniform(-0.8, 0.8), 4)
            
            budget = attr["budget"] + random.randint(-400, 500)
            temp = round(attr["temp"] + random.uniform(-3.0, 3.0), 1)
            pop = round(random.uniform(7.5, 9.6), 1)
            adv = min(10.0, max(2.0, round(attr["adventure"] + random.uniform(-0.8, 0.8), 1)))
            nat = min(10.0, max(2.0, round(attr["nature"] + random.uniform(-0.8, 0.8), 1)))
            nite = min(10.0, max(1.5, round(attr["nightlife"] + random.uniform(-0.8, 0.8), 1)))
            her = min(10.0, max(2.0, round(attr["heritage"] + random.uniform(-0.8, 0.8), 1)))
            pho = min(10.0, max(3.0, round(attr["photo"] + random.uniform(-0.6, 0.6), 1)))
            fam = random.choice([True, True, True, False])
            season = random.choice(["October - March", "September - May", "March - June", "November - February", "Year-round"])

            desc = f"A captivating travel destination in {state} renowned for its scenic beauty, distinctive {cat.lower()} attractions, vibrant local traditions, and peaceful surroundings."
            img = "https://images.unsplash.com/photo-1506461883276-594a12b11cf3?auto=format&fit=crop&w=800&q=80"
            if cat in ["Mountains", "Adventure"]:
                img = "https://images.unsplash.com/photo-1544644181-1484b3fdfc62?auto=format&fit=crop&w=800&q=80"
            elif cat in ["Beaches", "Nightlife"]:
                img = "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80"
            elif cat in ["Heritage", "Culture", "Spiritual"]:
                img = "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80"
            elif cat == "Wildlife":
                img = "https://images.unsplash.com/photo-1549366021-9f761d450615?auto=format&fit=crop&w=800&q=80"

            records.append({
                "destination_id": dest_id,
                "destination_name": town,
                "state": state,
                "country": "India",
                "category": cat,
                "average_budget": budget,
                "average_temperature": temp,
                "adventure_score": adv,
                "nature_score": nat,
                "nightlife_score": nite,
                "heritage_score": her,
                "photography_score": pho,
                "family_friendly": fam,
                "best_season": season,
                "popularity_score": pop,
                "latitude": jitter_lat,
                "longitude": jitter_lon,
                "description": desc,
                "image_url": img
            })
            existing_names.add(town)
            dest_id += 1

    df_dest = pd.DataFrame(records)
    os.makedirs("data/processed", exist_ok=True)
    os.makedirs("data/raw", exist_ok=True)
    df_dest.to_csv("data/processed/destinations.csv", index=False)
    print(f"Generated {len(df_dest)} destination records in data/processed/destinations.csv")

    # Generate Attractions for Destinations
    attractions = []
    attr_id = 1
    
    sample_activity_types = {
        "Mountains": [("Viewpoint Ridge", 2.0, 0, True), ("Pine Valley Trek", 3.5, 100, True), ("Monastery & Stupa", 1.5, 50, False), ("Local Mall Road Walk", 2.0, 0, True), ("Mountain Pass Look", 2.5, 0, True)],
        "Beaches": [("Golden Beach Promenade", 2.0, 0, True), ("Water Sports & Parasailing", 2.0, 800, True), ("Sunset Cliff Point", 1.5, 0, True), ("Heritage Portuguese Church", 1.5, 20, False), ("Flea & Night Market", 2.5, 0, True)],
        "Heritage": [("Grand Royal Palace", 3.0, 300, False), ("Ancient Hill Fort", 2.5, 150, True), ("Museum of Antiquities", 2.0, 100, False), ("Stepwell & Water Reservoir", 1.5, 50, True), ("Heritage Bazaar & Crafts", 2.0, 0, True)],
        "Adventure": [("River Rafting Rapid Point", 3.0, 1200, True), ("High Altitude Suspension Bridge", 1.5, 50, True), ("Zipline & Canopy Walk", 2.0, 750, True), ("Camping Ground & Bonfire", 4.0, 500, True), ("Rock Climbing Trail", 2.5, 400, True)],
        "Wildlife": [("Jungle Safari Zone", 3.5, 1500, True), ("Elephant Camp Observation", 2.0, 250, True), ("Interpretation Centre", 1.5, 80, False), ("Bird Watching Watchtower", 2.0, 100, True), ("River Nature Trail", 2.0, 50, True)],
        "Spiritual": [("Principal Temple & Shrines", 2.5, 0, False), ("Sacred River Ghat Walk", 1.5, 0, True), ("Evening Aarti Pavilion", 2.0, 0, True), ("Spiritual Meditation Ashram", 2.0, 100, False), ("Sacred Pond & Bathing Kund", 1.5, 0, True)],
        "Nature": [("Cascading Waterfalls", 2.0, 50, True), ("Botanical Flower Gardens", 2.0, 100, True), ("Eco Lake Boating", 2.0, 250, True), ("Forest Canopy Walk", 2.5, 150, True), ("Panoramic Sunrise Peak", 1.5, 0, True)],
        "Culture": [("Tribal Arts & Living Village", 2.5, 200, True), ("Folk Dance Amphitheatre", 2.0, 350, False), ("Old Quarter Walking Tour", 2.0, 0, True), ("Handicrafts Guild House", 2.0, 50, False), ("Culinary Tasting Street", 2.0, 0, True)],
        "Nightlife": [("Lively Beachfront Lounge", 3.0, 600, False), ("Sunset Cruise Deck", 2.5, 800, True), ("Night Flea Bazaar", 2.5, 0, True), ("Craft Brewery & Cafe", 2.0, 500, False), ("Music & Dance Club", 3.0, 1000, False)],
        "Food": [("Historic Food Street Walk", 2.5, 0, True), ("Traditional Sweetmakers Lane", 1.5, 0, True), ("Spice & Tea Plantation Tasting", 2.0, 200, True), ("Heritage Dining Hall", 2.0, 500, False), ("Local Morning Breakfast Hub", 1.5, 0, True)],
        "Photography": [("Golden Hour Scenic Overlook", 2.0, 0, True), ("Ancient Architecture Angle", 2.0, 50, True), ("Reflecting Alpine Waterbody", 2.0, 50, True), ("Dramatic Canyon Lookout", 2.0, 0, True), ("Vibrant Color Bazaar Street", 2.0, 0, True)]
    }

    for _, row in df_dest.iterrows():
        cat = row["category"]
        acts = sample_activity_types.get(cat, sample_activity_types["Nature"])
        for idx, (act_name, duration, fee, is_outdoor) in enumerate(acts, start=1):
            attractions.append({
                "attraction_id": attr_id,
                "destination_id": row["destination_id"],
                "destination_name": row["destination_name"],
                "name": f"{row['destination_name']} {act_name}",
                "category": cat,
                "description": f"Popular {act_name.lower()} in {row['destination_name']}, attracting travellers for scenic experiences and local discovery.",
                "estimated_duration_hours": duration,
                "entry_fee": fee,
                "is_outdoor": is_outdoor,
                "latitude": round(row["latitude"] + random.uniform(-0.04, 0.04), 4),
                "longitude": round(row["longitude"] + random.uniform(-0.04, 0.04), 4),
                "popularity_rank": idx,
                "image_url": row["image_url"]
            })
            attr_id += 1

    df_attr = pd.DataFrame(attractions)
    df_attr.to_csv("data/processed/attractions.csv", index=False)
    print(f"Generated {len(df_attr)} attraction records in data/processed/attractions.csv")

    # Generate Realistic Travel Expenses Training Data (3000 rows)
    # Target: total_trip_expense with realistic Indian travel component mathematics
    transport_rates = {"Flight": 6500, "Train": 1500, "Cab": 3200, "Bus": 900}
    hotel_rates = {"Budget": 1200, "Standard (3-star)": 2800, "Luxury (4/5-star)": 7500}
    season_multipliers = {"Off-peak": 0.85, "Moderate": 1.0, "Peak": 1.3}
    food_rates = {"Veg": 600, "Non-Veg": 900, "Both": 800}

    expense_records = []
    dest_names = df_dest["destination_name"].tolist()

    for i in range(3500):
        dest = random.choice(dest_names)
        dest_row = df_dest[df_dest["destination_name"] == dest].iloc[0]
        days = random.randint(2, 10)
        travellers = random.randint(1, 6)
        transport = random.choice(["Flight", "Train", "Cab", "Bus"])
        hotel = random.choice(["Budget", "Standard (3-star)", "Luxury (4/5-star)"])
        season = random.choice(["Off-peak", "Moderate", "Peak"])
        food = random.choice(["Veg", "Non-Veg", "Both"])
        sightseeing_count = random.randint(2, days * 3)

        # Baseline cost calculations with realistic noise
        season_mult = season_multipliers[season]
        
        # Transport: base per traveller round trip
        transport_cost = transport_rates[transport] * travellers * random.uniform(0.9, 1.15)
        if transport == "Flight" and days <= 3:
            transport_cost *= 1.1

        # Accommodation: rooms needed = ceil(travellers / 2)
        rooms = (travellers + 1) // 2
        hotel_cost = hotel_rates[hotel] * rooms * (days - 1 if days > 1 else 1) * season_mult * random.uniform(0.92, 1.08)

        # Food: per person per day
        food_cost = food_rates[food] * travellers * days * random.uniform(0.9, 1.12)

        # Sightseeing: entry fees + local transport
        sightseeing_cost = (sightseeing_count * 250 + 400 * days) * travellers * random.uniform(0.85, 1.15)

        # Misc: shopping, emergency, snacks
        misc_cost = (500 * days + 300 * travellers) * random.uniform(0.8, 1.25)

        total_expense = round(transport_cost + hotel_cost + food_cost + sightseeing_cost + misc_cost, 2)

        expense_records.append({
            "destination": dest,
            "destination_category": dest_row["category"],
            "duration_days": days,
            "travellers_count": travellers,
            "transport_mode": transport,
            "hotel_category": hotel,
            "season": season,
            "food_preference": food,
            "sightseeing_count": sightseeing_count,
            "transportation_expense": round(transport_cost, 2),
            "accommodation_expense": round(hotel_cost, 2),
            "food_expense": round(food_cost, 2),
            "sightseeing_expense": round(sightseeing_cost, 2),
            "miscellaneous_expense": round(misc_cost, 2),
            "total_trip_expense": total_expense
        })

    df_expenses = pd.DataFrame(expense_records)
    df_expenses.to_csv("data/processed/travel_expenses.csv", index=False)
    print(f"Generated {len(df_expenses)} expense records in data/processed/travel_expenses.csv")

    # Generate Crowd Levels Dataset (Historical & Seasonal Tourist Footfalls)
    # Features: destination, month, day_of_week, is_weekend, is_public_holiday, season -> crowd_level (Low, Medium, High)
    crowd_records = []
    seasons_by_month = {
        12: "Winter", 1: "Winter", 2: "Winter",
        3: "Spring", 4: "Summer", 5: "Summer", 6: "Monsoon",
        7: "Monsoon", 8: "Monsoon", 9: "Autumn", 10: "Autumn", 11: "Winter"
    }

    for i in range(4000):
        dest = random.choice(dest_names[:50])  # top 50 popular destinations
        dest_row = df_dest[df_dest["destination_name"] == dest].iloc[0]
        month = random.randint(1, 12)
        day_of_week = random.randint(0, 6)
        is_weekend = 1 if day_of_week in [5, 6] else 0
        is_holiday = 1 if random.random() < 0.08 else 0
        season = seasons_by_month[month]

        # Calculate crowd propensity score
        score = dest_row["popularity_score"] * 0.4
        
        # Season alignment with destination best season
        if dest_row["category"] in ["Mountains", "Adventure"] and month in [5, 6, 10]:
            score += 3.5
        elif dest_row["category"] in ["Beaches", "Nightlife"] and month in [11, 12, 1]:
            score += 4.0
        elif dest_row["category"] in ["Heritage", "Spiritual"] and month in [10, 11, 12, 1, 2]:
            score += 3.0
        elif month in [7, 8]:  # monsoon drop in hills
            score -= 1.5

        if is_weekend:
            score += 1.8
        if is_holiday:
            score += 2.2

        score += random.uniform(-0.8, 0.8)

        if score > 8.5:
            crowd = "High"
        elif score > 6.0:
            crowd = "Medium"
        else:
            crowd = "Low"

        crowd_records.append({
            "destination": dest,
            "month": month,
            "day_of_week": day_of_week,
            "is_weekend": is_weekend,
            "is_public_holiday": is_holiday,
            "season": season,
            "crowd_score": round(min(1.0, max(0.1, score / 12.0)), 2),
            "crowd_level": crowd
        })

    df_crowd = pd.DataFrame(crowd_records)
    df_crowd.to_csv("data/processed/historical_visitors.csv", index=False)
    print(f"Generated {len(df_crowd)} crowd records in data/processed/historical_visitors.csv")

    # Generate RAG Knowledge Base Articles
    rag_dir = "rag_knowledge_base/destinations"
    os.makedirs(rag_dir, exist_ok=True)
    
    for _, row in df_dest.head(45).iterrows():
        filename = f"{rag_dir}/{row['destination_name'].lower().replace(' ', '_')}.md"
        content = f"""# {row['destination_name']}, {row['state']}
**Category:** {row['category']}  
**Best Season to Visit:** {row['best_season']}  
**Average Daily Budget:** INR {row['average_budget']} per person  
**Average Temperature:** {row['average_temperature']} °C  

## Overview
{row['description']}

## Key Tourist Attractions
- Sightseeing Highlights: Exploration of cultural monuments, viewpoints, and nature trails.
- Unique Landmarks: Signature heritage and scenic points celebrated across {row['state']}.
- Outdoor Activities: Trekking, boating, photography, and local market strolling.

## Cultural & Historical Context
{row['destination_name']} has deep regional heritage representing the cultural vibrancy of {row['state']}. Local residents celebrate regional festivals with music, handloom crafts, and authentic cuisine.

## Local Food Recommendations
Travellers visiting {row['destination_name']} should savor authentic regional delicacies, street food specialities, and seasonal sweets available at traditional market hubs.

## Travel Tips & Safety Guidelines
- Recommended Duration: 3 to 5 days.
- Best Transportation: Well connected by road, rail, and nearby airport terminals.
- Weather Preparation: Carry light woollens in winter or high-altitude evenings; carry rain gear if visiting during monsoon.
- Eco-Tourism: Keep natural trails clean and respect local heritage sites.
"""
        with open(filename, "w", encoding="utf-8") as f:
            f.write(content)
            
    print(f"Generated RAG knowledge base markdown articles in {rag_dir}")


if __name__ == "__main__":
    build_full_dataset()
