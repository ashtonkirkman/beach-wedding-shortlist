#!/usr/bin/env python3
"""Generate the March (new version) and January wedding shortlist pages from one template."""
import json, html

OUT = '/tmp/claude-1000/-mnt-c-Users-AshtonKirkman-Downloads/266650cc-f533-48a3-9370-472c6617543a/scratchpad/'

def air(room, ci, co):
    return f"https://www.airbnb.com/rooms/{room}?adults=16&check_in={ci}&check_out={co}"

def fly(apt, ci, co, nonstop=False):
    q = f"Flights%20from%20SLC%20to%20{apt}%20on%20{ci}%20through%20{co}"
    if nonstop: q += "%20nonstop"
    return f"https://www.google.com/travel/flights?q={q}"

def money(n): return f"${n:,}"

def opt(n, key, name, sub, ll, place, apt, ci, co, aptcode, rental, fare, fareS, chips, warn, take, pros, cons,
        nonstop=None, nonstopS=None, off=None, extra=0, extraS=None):
    nights = 3
    d = dict(n=n, key=key, name=name, sub=sub, ll=ll, place=place, apt=apt, ci=ci, co=co,
             dates=fmt_dates(ci, co), rental=money(rental), night=money(round(rental / nights)),
             fare=money(fare), fareS=fareS, couple=money(rental + 2 * fare + extra),
             chips=chips, warn=warn, take=take, pros=pros, cons=cons,
             air=air(key_room[key], ci, co), fly=fly(aptcode, ci, co), off=off or [0, 0])
    if nonstop:
        d['nonstop'] = money(nonstop); d['nonstopS'] = nonstopS; d['flyNS'] = fly(aptcode, ci, co, True)
        d['coupleNS'] = money(rental + 2 * nonstop + extra)
    if extra:
        d['extraS'] = extraS
    return d

MONTHS = {1: 'Jan', 3: 'Mar'}
DOW = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
import datetime
def fmt_dates(ci, co):
    a = datetime.date.fromisoformat(ci); b = datetime.date.fromisoformat(co)
    return f"{DOW[a.weekday()]} {MONTHS[a.month]} {a.day} to {DOW[b.weekday()]} {MONTHS[b.month]} {b.day}"

key_room = {
    'dorada': '43350753', 'spring': '15182252', 'roatan': '33930767', 'volley': '1207608858677914583',
    'flora': '13232422', 'marbello': '959450217767207749', 'pinos': '1040732860347668289',
    'hotelzone': '1762169411988617642', 'tuscania': '1397106283816214549',
}

# ---------------------------------------------------------------- shared option text
DORADA_PROS = ['Cheapest qualifying house in either month, with a private pool',
               'Zona Dorada: cafés, bars and the beach all within a short walk',
               '4.95 across 191 reviews, Superhost', 'Seven bedrooms, 6.5 baths for 16',
               'Mazatlán is roughly 75°F with 72°F water in both months']
DORADA_CONS = ['Three blocks from the sand, not beachfront', 'No nonstop from Salt Lake City; one stop through Dallas or Phoenix',
               'Cleaning staff come in daily and the host is particular, per reviews', 'Listing says nothing about events; ask before relying on it',
               'Only 11 beds, so some guests double up']
FLORA_PROS = ['Host explicitly welcomes wedding parties and reunions', 'Main house plus two casitas, private pool and tennis court',
              'Los Cabos has the cheapest fares of any international airport here, nonstop or one stop', 'Three minutes over the dunes to a wide, empty Pacific beach', '4.82 across 50 reviews']
FLORA_CONS = ['Pacific surf beach: a walking and ceremony beach, not a swimming beach', 'Public beach path crosses the property',
              'About 75 minutes from the airport', 'Todos Santos is cooler at night than the Sea of Cortez side']
VOLLEY_PROS = ['Cheapest beachfront house of the whole sweep', 'First row on the sand with a private pool and volleyball court',
               '4.97 across 29 reviews, Superhost', 'Forty-five minutes from the airport, near El Tunco and El Zonte']
VOLLEY_CONS = ['Only 3 bathrooms for 16 guests', 'Twelve double beds, so everyone shares a bed',
               'San Salvador fares are the highest on this list; one stop through Houston or Dallas', 'Pacific surf beach with currents',
               'Listing says nothing about events; ask the host']
TUSCANIA_PROS = ['Weddings allowed in writing, for an added fee', '18 beds and room for 25 guests', 'Oceanfront, steps to the sand, private pool',
                 '4.86 across 73 reviews, Superhost', 'Twenty-five minutes from the airport']
TUSCANIA_CONS = ['San Salvador fares are about $1,000 a seat', 'Pacific surf beach', 'Six baths for 16', '$300 cash deposit; surcharge above 16 guests']

# ---------------------------------------------------------------- JANUARY
JAN = dict(
    title='January Beach Wedding',
    eyebrow='Destination wedding · January 2027',
    h1='Six places to say it <em>on the sand</em> in January',
    brief=['<b>16 guests</b> in one rental', '<b>3 nights</b> · any window Jan 1 to 10, 2027',
           'Flights from <b>Salt Lake City</b>', 'Ranked by what the <b>bride and groom</b> pay'],
    lede=("Ranked by the couple's own bill: the whole rental plus two round-trip seats from Salt Lake City. "
          "A sweep of about 60 beach towns and 48 airports across Mexico, Central America, the Caribbean, Florida and Hawaii, "
          "roughly 1,100 listing cards, with the top 60 opened to confirm price, beach access and event rules. "
          "Every option sleeps 16 or more, rates 4.8 or better, and is on or within a couple of minutes of a beach. "
          "Fares are live Google Flights prices pulled Oct 1, 2026 for the exact dates. The first three days of January still carry "
          "holiday pricing, so every pick lands on Jan 4 or later."),
    map_sub='Arcs show the flight from SLC. Each card lists the cheapest sane routing for the exact dates.',
    rank_h2='The shortlist, in order of what the couple pays',
    rank_p=("Couple's total = Airbnb total for 16 adults on the dates shown (before local lodging tax) + two round-trip fares. "
            "Fares are single-seat Google Flights prices for those dates, nonstop or one connection under 10 hours door to door "
            "with a layover under 4 hours, and exclude about $80 for a checked bag."),
    tags=[dict(ll=[-106.42, 23.24], text='Mazatlán', dx=14, dy=28, anchor='middle'),
          dict(ll=[-110.22, 23.45], text='Todos Santos', dx=-16, dy=5, anchor='end'),
          dict(ll=[-101.55, 17.64], text='Zihuatanejo', dx=0, dy=26, anchor='middle'),
          dict(ll=[-86.58, 16.33], text='Roatán', dx=20, dy=5, anchor='start'),
          dict(ll=[-89.32, 13.49], text='La Libertad, El Salvador', dx=0, dy=28, anchor='middle')],
    options=[
        opt(1, 'dorada', 'Casa Dorada', 'Golden Zone villa with a private pool, three blocks from the beach',
            [-106.44, 23.27], 'Zona Dorada, Mazatlán, Sinaloa, Mexico', 'MZT · about 25 min drive',
            '2027-01-07', '2027-01-10', 'MZT', 1496, 757, 'American via Dallas, 6 h 27 min, 44-min layover',
            ['4-min walk to a calm beach', 'Private pool', 'Sleeps 16+ · 7 BR · 11 beds · 6.5 baths', '4.95 · 191 reviews'],
            ['Events not stated', 'Jan 1 to 4 not available'],
            "<b>The cheapest bill for the couple in either month.</b> Mazatlán's Golden Zone puts a whole seven-bedroom house with a private pool under $500 a night, and the beach is three short blocks away. The trade is that there is no nonstop from Salt Lake City, so the two of you connect through Dallas or Phoenix. Jan 4 to 7 prices the same; Jan 1 to 4 is blocked.",
            DORADA_PROS, DORADA_CONS, off=[0, 0]),
        opt(2, 'spring', 'The Spring, Playa La Madera', 'Beachfront house with pool and fire pit on a calm bay',
            [-101.55, 17.64], 'Playa La Madera, Zihuatanejo, Guerrero, Mexico', 'ZIH · 15 to 20 min drive',
            '2027-01-04', '2027-01-07', 'ZIH', 1538, 902, 'American via Dallas, 6 h 38 min, 50-min layover',
            ['Beachfront, calm swimmable bay', 'Pool shared with the other units on the property', 'Sleeps 16+ · 6 BR · 11 beds · 5 baths', '4.81 · 109 reviews', 'Firepit on the sand'],
            ['Events not stated', 'Pool is small and shared'],
            "<b>The warmest water on the list.</b> Zihuatanejo in January is about 88°F with 80°F water, and this house opens straight onto the sand of a calm bay in the old fishermen's neighbourhood. It is the cheapest true beachfront house found anywhere. Reviews warn that the pool is small and shared with two smaller apartments on the same property, so check whether the host will rent the whole compound.",
            ['Cheapest true beachfront house of the sweep', 'Calm bay you can swim in, 80°F water', 'Fire pit on the beach; host can arrange a campfire', 'Fifteen minutes from the airport, walk to town', 'Same price Jan 7 to 10'],
            ['Pool and common areas are shared with two smaller units', 'Rating is 4.81, just over the bar', 'Zihuatanejo fares run about $900 a seat, one stop through Dallas', 'Rooms must be vacated at 9 am on checkout day, per a review', 'Charges about 350 pesos a night per person above 16']),
        opt(3, 'roatan', 'Sandy Bay Beachfront Villas', 'Up to five villas on one beachfront lot with a dock and pool',
            [-86.58, 16.33], 'Sandy Bay, Roatán, Honduras', 'RTB · about 20 min drive',
            '2027-01-04', '2027-01-07', 'RTB', 1840, 854, 'American via Dallas, 6 h 52 min, 49-min layover',
            ['Beachfront, calm Caribbean water', 'Private pool and dock', 'Sleeps 16+ · 13 BR · 14 beds · 12 baths', '4.88 · 16 reviews', 'A past guest held a wedding here'],
            ['Confirm the price covers all villas', 'Events not stated'],
            "<b>The Caribbean pick.</b> Turquoise water, a reef a short swim out, and more bathrooms than any other house here. The listing bundles one to five villas and its title says pricing is on request, so the $1,840 shown for 16 adults must be confirmed with the host before you count on it. A guest review describes a wedding held right out front.",
            ['Calm, clear Caribbean water and snorkelling off the dock', 'Twelve bathrooms and 13 bedrooms for 16', 'Only 20 minutes from the airport', 'Private pool', 'A review mentions a wedding on the beach here'],
            ['Price must be confirmed for the full compound', 'Only 16 reviews', 'January is the tail of Roatán\'s rainy season, with brief showers', 'One stop through Dallas; no nonstop', 'Not available in the March window']),
        opt(4, 'volley', 'Beachfront House with Pool and Volleyball', 'First-row surf-beach house, 45 minutes from San Salvador',
            [-89.32, 13.49], 'La Libertad, El Salvador', 'SAL · about 45 min drive',
            '2027-01-07', '2027-01-10', 'SAL', 1425, 1128, 'United via Houston, 7 h 39 min, 1 h 24 min layover',
            ['Beachfront, Pacific surf', 'Private pool and volleyball court', 'Sleeps 16+ · 6 BR · 12 beds · 3 baths', '4.97 · 29 reviews'],
            ['Only 3 bathrooms', 'Events not stated'],
            "<b>The cheapest beachfront house found, with a catch.</b> Under $500 a night for a first-row house with its own pool and sand volleyball court, but only three bathrooms for 16 people, and San Salvador fares are the highest here. If the bathroom count is a dealbreaker, Villa Marbello below is the better El Salvador house.",
            VOLLEY_PROS, VOLLEY_CONS),
        opt(5, 'flora', 'Flora del Mar', 'Main house and two casitas with pool, three minutes over the dunes',
            [-110.22, 23.45], 'Todos Santos, Baja California Sur, Mexico', 'SJD · about 1 h 15 min drive',
            '2027-01-04', '2027-01-07', 'SJD', 2475, 625, 'Southwest via Phoenix, 6 h 35 min, 2 h 45 min layover',
            ['3-min walk, Pacific surf', 'Private pool and tennis court', 'Sleeps 16+ · 6 BR · 11 beds · 6.5 baths', '4.82 · 50 reviews', 'Weddings welcomed in writing'],
            ['Beach not swimmable'],
            "<b>The one that says yes to weddings.</b> Flora del Mar welcomes wedding parties in its listing, has room to spread 16 people over three buildings, and sits on the cheapest fare route of any international airport in the sweep, with a Delta nonstop for $15 more a seat. The beach is a wide, empty Pacific stretch for a ceremony and photos, not for swimming.",
            FLORA_PROS, FLORA_CONS, nonstop=640, nonstopS='Delta nonstop, 3 h 20 min'),
        opt(6, 'marbello', 'Villa Marbello', 'Beachfront villa with private beach, pool and jacuzzi',
            [-89.25, 13.47], 'Playa San Diego, La Libertad, El Salvador', 'SAL · about 30 min drive',
            '2027-01-04', '2027-01-07', 'SAL', 1602, 1119, 'American via Dallas, 7 h 43 min, 1 h 20 min layover',
            ['Beachfront, private beach', 'Private pool and jacuzzi', 'Sleeps 16+ · 7 BR · 13 beds · 7.5 baths', '4.9 · 302 reviews', 'Small parties OK by the pool'],
            ['About $180 in extra-guest fees', 'Not available in March'],
            "<b>The best-reviewed cheap house.</b> Three hundred reviews at 4.9, seven and a half baths, a private beach and pool, all for $534 a night before an extra-guest surcharge the host collects in cash. Small gatherings in the pool area are fine; a full wedding needs the owner's approval first.",
            ['302 reviews at 4.9, Superhost', 'Private beach and pool, 7.5 baths for 16', 'Thirty minutes from the airport', 'Small parties allowed in writing', 'Base price covers 12, so the surcharge is modest'],
            ['San Salvador fares around $1,100 a seat', 'Extra-guest fee of $15 a night per guest above 12, cash at check-in', 'Large parties need owner pre-approval', 'Pacific surf beach', 'Kitchen is self-clean; on-site restaurant is third party'],
            off=[28, 0], extra=180, extraS='includes about $180 in extra-guest fees'),
    ],
    notes_a=dict(h='How the numbers were built', items=[
        '<b>Lodging</b> is the total Airbnb displayed for 16 adults on the exact dates, before local tax. Expect roughly 16 to 19 percent on top in Mexico and El Salvador, and about 19 percent in Honduras.',
        '<b>Fares</b> are live Google Flights prices for one seat on the exact dates, pulled Oct 1, 2026. Only nonstops and single connections under 10 hours with layovers under 4 hours count. Add about $80 a person for a checked bag.',
        '<b>Dates</b> matter more than usual. Jan 1 to 3 is still holiday pricing: Tuscania House in El Salvador is $2,904 for Jan 4 to 7 but $2,344 for Jan 7 to 10, and fares to Mexico drop $100 to $300 after Jan 3. Nothing here is available Jan 1 to 4.',
        '<b>Skipped on purpose:</b> Hawaii (no legal 16-person beach rental under $7,400), Florida (Destin houses are $1,559 to $1,794 but ban events and the Gulf is 58°F in January), Costa Rica, Panama, Nicaragua, Punta Cana, Aruba, Turks and Caicos and the Bahamas (nothing beachfront for 16 under $5,000), and Cartagena (no routing under 10 hours).']),
    notes_b=dict(h='Just missed the list', items=[
        '<b>Villa La Jolla</b>, East Cape: $2,686 + two $625 seats = <b>$3,936</b>. The old March favourite is only open Jan 4 to 7 and lands seventh on cost.',
        '<b>Costa Paraíso</b>, Aguada, Puerto Rico: $2,887 + two $798 seats = <b>$4,483</b> for Jan 7 to 10. Oceanfront, 4.91 over 216 reviews, no passport.',
        '<b>Sharkfin Villa</b>, Duncans, Jamaica: $3,255 + two $783 seats = <b>$4,821</b>. Cook and housekeeper included, markets itself to weddings.',
        '<b>Villa Kaisa</b>, La Cruz: $3,549 + two $680 nonstops = <b>$4,909</b>. Still the most complete wedding house if the budget stretches.',
        '<b>Casa de Playa Tortugas</b>, Isla Blanca: $4,476 + two $725 seats = <b>$5,926</b>, Jan 7 to 10 only.']),
    notes_c=dict(h='Before booking', items=[
        'Message every host about a ceremony and amplified music. Only Flora del Mar says yes in writing; Villa Marbello allows small parties and wants approval for anything larger.',
        'Confirm the Sandy Bay price covers all five villas, and ask The Spring whether the two smaller apartments can be included so the pool is yours.',
        'Fares are single-seat prices. For 16 seats on one plane, get quotes from Delta\'s group desk (800-532-4777) and American\'s (800-433-1790).',
        'Guests flying from elsewhere lose the Dallas and Phoenix connections priced here; check their home airports before fixing the destination.']),
)

# ---------------------------------------------------------------- MARCH (new version)
MAR = dict(
    title='Beach Wedding Shortlist',
    eyebrow='Destination wedding · March 2027 · version 2',
    h1='Six places to say it <em>on the sand</em>',
    brief=['<b>16 guests</b> in one rental', '<b>3 nights</b> · any window Mar 11 to 15, 2027',
           'Flights from <b>Salt Lake City</b>', 'Ranked by what the <b>bride and groom</b> pay'],
    lede=("Re-run for the new dates and a new goal. The first version ranked by group airfare; this one ranks by the couple's own bill: "
          "the whole rental plus two round-trip seats from Salt Lake City. Same bar as before: sleeps 16 or more, rated 4.8 or better, "
          "on or within a couple of minutes of a beach. About 60 towns and 48 airports swept, roughly 1,100 listing cards, the top 60 opened "
          "to confirm price, beach access and event rules. Fares are live Google Flights prices pulled Oct 1, 2026 for the exact dates. "
          "Returning Sunday Mar 14 or Monday Mar 15 keeps everyone well clear of the Holy Week surge that starts Mar 19."),
    map_sub='Arcs show the flight from SLC. Each card lists the cheapest sane routing for the exact dates.',
    rank_h2='The shortlist, in order of what the couple pays',
    rank_p=("Couple's total = Airbnb total for 16 adults on the dates shown (before local lodging tax) + two round-trip fares. "
            "Fares are single-seat Google Flights prices for those dates, nonstop or one connection under 10 hours door to door "
            "with a layover under 4 hours, and exclude about $80 for a checked bag."),
    tags=[dict(ll=[-106.42, 23.24], text='Mazatlán', dx=14, dy=28, anchor='middle'),
          dict(ll=[-110.22, 23.45], text='Todos Santos', dx=-16, dy=5, anchor='end'),
          dict(ll=[-86.77, 21.08], text='Cancún Hotel Zone', dx=0, dy=-17, anchor='middle'),
          dict(ll=[-89.32, 13.49], text='La Libertad, El Salvador', dx=0, dy=28, anchor='middle')],
    options=[
        opt(1, 'pinos', 'Pinos Beachfront Apartments', 'Two stacked floors, eight ensuite bedrooms, right on Playa Los Pinos',
            [-106.42, 23.20], 'Olas Altas, Mazatlán, Sinaloa, Mexico', 'MZT · about 30 min drive',
            '2027-03-12', '2027-03-15', 'MZT', 1420, 733, 'Delta and Aeroméxico via Mexico City, 7 h 21 min, 1 h 15 min layover',
            ['Beachfront, small surf beach', 'Every bedroom has its own bath', 'Sleeps 21 · 8 BR · 9 beds · 9 baths', '5.0 · 7 reviews', 'Steps from the Malecón'],
            ['No pool', 'Only 7 reviews', 'No smoke or CO alarm listed'],
            "<b>The lowest bill for the couple.</b> Under $475 a night for a beachfront building where all eight bedrooms have their own bathroom, two blocks from the old town and the Malecón. There is no pool and the beach in front is a small surf break, so this is the pick if the ocean view and the price matter more than a swim.",
            ['Cheapest couple\'s total of the whole sweep', 'Beachfront, with the Malecón and old-town restaurants at the door', 'Nine bathrooms, one per bedroom', 'Same price Mar 11 to 14', 'Mazatlán is dry and about 79°F in March'],
            ['No pool', 'Small surf beach rather than a calm bay', 'Only 7 reviews, though all five stars', 'No nonstop; one stop through Mexico City or Phoenix', 'Four-night minimum in January, so March only'],
            off=[0, 0]),
        opt(2, 'dorada', 'Casa Dorada', 'Golden Zone villa with a private pool, three blocks from the beach',
            [-106.44, 23.27], 'Zona Dorada, Mazatlán, Sinaloa, Mexico', 'MZT · about 25 min drive',
            '2027-03-12', '2027-03-15', 'MZT', 1933, 733, 'Delta and Aeroméxico via Mexico City, 7 h 21 min, 1 h 15 min layover',
            ['4-min walk to a calm beach', 'Private pool', 'Sleeps 16+ · 7 BR · 11 beds · 6.5 baths', '4.95 · 191 reviews'],
            ['Events not stated'],
            "<b>The safer Mazatlán house.</b> Nearly 200 reviews at 4.95, a private pool, and the Golden Zone's calm beach three blocks away. It costs about $500 more than Pinos over three nights and buys a pool, a track record and a swimmable beach. Mar 11 to 14 is $54 cheaper on the house but $80 more a seat.",
            DORADA_PROS, DORADA_CONS, off=[28, 0]),
        opt(3, 'volley', 'Beachfront House with Pool and Volleyball', 'First-row surf-beach house, 45 minutes from San Salvador',
            [-89.32, 13.49], 'La Libertad, El Salvador', 'SAL · about 45 min drive',
            '2027-03-11', '2027-03-14', 'SAL', 1632, 1007, 'American via Dallas, 7 h 44 min, 1 h 28 min layover',
            ['Beachfront, Pacific surf', 'Private pool and volleyball court', 'Sleeps 16+ · 6 BR · 12 beds · 3 baths', '4.97 · 29 reviews'],
            ['Only 3 bathrooms', 'Events not stated'],
            "<b>The cheapest beachfront house found, with a catch.</b> About $545 a night for a first-row house with its own pool and sand volleyball court, but only three bathrooms for 16 people. San Salvador fares are the highest on this page, which is why a $1,632 house ranks third rather than first.",
            VOLLEY_PROS, VOLLEY_CONS),
        opt(4, 'hotelzone', 'Hotel Zone Oceanfront Villa', 'Three-level villa on the sand near Playa Delfines',
            [-86.77, 21.08], 'Hotel Zone, Cancún, Quintana Roo, Mexico', 'CUN · about 25 min drive',
            '2027-03-12', '2027-03-15', 'CUN', 2306, 724, 'Southwest via Phoenix, 8 h 35 min, 2 h 55 min layover',
            ['Beachfront, wide sandy Caribbean beach', 'Private pool', 'Sleeps 16+ · 6 BR · 11 beds · 4 baths', 'New listing · 2 reviews', '24/7 security'],
            ['Brand new listing', '4 baths for 16'],
            "<b>The Caribbean pick.</b> A private entrance straight onto Cancún's best public beach, a pool, two full kitchens and a Delta nonstop if you pay $130 more a seat. It is brand new with two reviews, so there is no track record yet, and four bathrooms is tight for 16.",
            ['On the sand, turquoise Caribbean water', 'Twenty-five minutes from the airport, nonstop available', 'Private pool, two kitchens, 24-hour security', 'Cheaper than any other beachfront house with a pool on this page'],
            ['Only 2 reviews', 'Four bathrooms for 16', 'Cancún nonstop is at spring-break peak pricing', 'Hotel Zone traffic and resort crowds', 'Listing says nothing about events'],
            nonstop=856, nonstopS='Delta nonstop, 4 h 30 min'),
        opt(5, 'flora', 'Flora del Mar', 'Main house and two casitas with pool, three minutes over the dunes',
            [-110.22, 23.45], 'Todos Santos, Baja California Sur, Mexico', 'SJD · about 1 h 15 min drive',
            '2027-03-12', '2027-03-15', 'SJD', 2475, 720, 'Alaska via San Diego, 6 h 29 min, 1 h 57 min layover',
            ['3-min walk, Pacific surf', 'Private pool and tennis court', 'Sleeps 16+ · 6 BR · 11 beds · 6.5 baths', '4.82 · 50 reviews', 'Weddings welcomed in writing'],
            ['Beach not swimmable'],
            "<b>The one that says yes to weddings.</b> Flora del Mar welcomes wedding parties in its listing, spreads 16 people over three buildings, and Los Cabos remains the cheapest international fare from Salt Lake City, with a Delta nonstop for $24 more a seat. The beach is a wide Pacific stretch for a ceremony and photos rather than swimming.",
            FLORA_PROS, FLORA_CONS, nonstop=744, nonstopS='Delta nonstop, 3 h 13 min'),
        opt(6, 'tuscania', 'Tuscania House', 'Oceanfront villa with pool, weddings allowed',
            [-89.40, 13.48], 'Playa Cangrejera, La Libertad, El Salvador', 'SAL · about 25 min drive',
            '2027-03-11', '2027-03-14', 'SAL', 1976, 1007, 'American via Dallas, 7 h 44 min, 1 h 28 min layover',
            ['Oceanfront', 'Private pool', 'Sleeps 25 · 6 BR · 18 beds · 6 baths', '4.86 · 73 reviews', 'Weddings allowed for a fee'],
            ['Surcharge above 16 guests', '$300 cash deposit'],
            "<b>Still the only cheap house with weddings in writing.</b> Version one's number two. The house is $176 more than it was for Mar 16 to 19, and San Salvador fares have come in at about $1,000 a seat, so it slips to sixth on the couple's bill while staying the easiest place to actually hold the ceremony.",
            TUSCANIA_PROS, TUSCANIA_CONS, off=[28, 0]),
    ],
    notes_a=dict(h='How the numbers were built', items=[
        '<b>Lodging</b> is the total Airbnb displayed for 16 adults on the exact dates, before local tax. Expect roughly 16 to 19 percent on top in Mexico and El Salvador.',
        '<b>Fares</b> are live Google Flights prices for one seat on the exact dates, pulled Oct 1, 2026. Only nonstops and single connections under 10 hours with layovers under 4 hours count. Add about $80 a person for a checked bag.',
        '<b>Dates.</b> Thursday Mar 11 departures are $50 to $150 cheaper to Mexico than Friday Mar 12 on most routes, and Mazatlán houses price the same either way. Both windows return before Holy Week (Mar 21 to 28) and before the Friday Mar 19 travel surge.',
        '<b>Skipped on purpose:</b> Hawaii (nothing legal for 16 on a beach under $7,400), Florida (Destin at $2,146 bans parties and the Gulf is 63°F), Costa Rica, Panama, Nicaragua, Punta Cana, Aruba, the Bahamas and Turks and Caicos (nothing beachfront for 16 under $5,000), and Carlsbad (cold).',
        '<b>Wildcard:</b> La Catalina Plus near Cartagena, Colombia, is $1,203 for Mar 12 to 15, eight bedrooms with a pool two minutes from the beach, so the couple\'s total would be about $2,767. It fails the layover rule (12 hours through Miami), has 5 reviews, and events need host approval, so it is not ranked.']),
    notes_b=dict(h='Where version one\'s five landed', items=[
        '<b>Villa La Jolla</b>, East Cape: $2,686 + two $720 seats = <b>$4,126</b>. Still the cheapest calm-water beachfront house, now seventh on the couple\'s bill.',
        '<b>Tuscania House</b>: now sixth, above.',
        '<b>Villa Kaisa</b>, La Cruz: $3,549 + two $772 nonstops = <b>$5,093</b>. Same price both windows. Still the most complete wedding house if the budget stretches.',
        '<b>Tropical Beach Oasis</b>, Luquillo: $3,157 + two $756 seats = <b>$4,669</b>.',
        '<b>Casa de Playa Tortugas</b>, Isla Blanca: $4,476 + two $724 seats = <b>$5,924</b>. Weddings and staff included, but the most expensive bill here.']),
    notes_c=dict(h='Before booking', items=[
        'Message every host about a ceremony and amplified music. Only Flora del Mar and Tuscania House say yes in writing.',
        'Fares are single-seat prices. For 16 seats on one plane, get quotes from Delta\'s group desk (800-532-4777) and American\'s (800-433-1790).',
        'Pinos has no smoke or carbon-monoxide alarm listed and no pool; weigh that against the $500 saving over Casa Dorada.',
        'Guests flying from elsewhere lose the Dallas and Mexico City connections priced here; check their home airports before fixing the destination.']),
)

# ---------------------------------------------------------------- template
CSS = r"""
/* Layout: a travel brief. One regional map up top with numbered pins and flight arcs from SLC,
   then ranked option cards, each carrying its own mini map, the four numbers that matter
   (rental, per night, fare, the couple's total), pros and cons, and the booking links. */
:root{
  --bg:#F3F7F6; --surface:#FFFFFF; --fg:#17323B; --muted:#5C7680; --line:#D3DFDF;
  --accent:#0F6F7C; --accent-soft:#DCEFF0; --sun:#C08A22; --sun-soft:#F7ECD3;
  --ocean:#DCEAEB; --land:#CBD7D1; --land-line:#B3C3BC; --arc:#0F6F7C;
  --good:#2E7D4F; --bad:#B9483A;
  --display:"Instrument Serif", Georgia, "Times New Roman", serif;
  --body:"Instrument Sans", system-ui, -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#0E1B1F; --surface:#15262B; --fg:#E5EEEF; --muted:#94AAB0; --line:#263B41;
    --accent:#63C4CF; --accent-soft:#15343B; --sun:#E1B35B; --sun-soft:#2E2816;
    --ocean:#10252B; --land:#2A4048; --land-line:#3A535B; --arc:#63C4CF;
    --good:#5FC38A; --bad:#EE8A7A; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#0E1B1F; --surface:#15262B; --fg:#E5EEEF; --muted:#94AAB0; --line:#263B41;
  --accent:#63C4CF; --accent-soft:#15343B; --sun:#E1B35B; --sun-soft:#2E2816;
  --ocean:#10252B; --land:#2A4048; --land-line:#3A535B; --arc:#63C4CF;
  --good:#5FC38A; --bad:#EE8A7A; color-scheme:dark;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);font-family:var(--body);font-size:16px;line-height:1.5;margin:0}
.wrap{max-width:1040px;margin:0 auto;padding-inline:20px;padding-block:32px 56px}
a{color:var(--accent)}
a:focus-visible,button:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.eyebrow{font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}
h1{font-family:var(--display);font-weight:400;font-size:clamp(40px,7vw,68px);line-height:1;margin:6px 0 14px;text-wrap:balance;letter-spacing:-.01em}
h1 em{font-style:italic;color:var(--accent)}
.brief{display:flex;flex-wrap:wrap;gap:10px 28px;color:var(--muted);font-size:15px;max-width:70ch}
.brief b{color:var(--fg);font-weight:600}
.lede{max-width:66ch;font-size:17px;margin:22px 0 0}
.map-card{margin-top:34px;background:var(--surface);border:1px solid var(--line);border-radius:14px;overflow:hidden}
.map-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:baseline;gap:8px 20px;padding:16px 20px 0}
.map-head h2{font-family:var(--display);font-weight:400;font-size:28px;margin:0}
.map-head p{margin:0;color:var(--muted);font-size:14px}
.map-card svg{display:block;width:100%;height:auto;background:var(--ocean)}
.legend{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:8px 18px;padding:14px 20px 18px;border-top:1px solid var(--line)}
.legend div{display:flex;gap:10px;align-items:center;font-size:14px}
.legend .n{flex:none;width:24px;height:24px;border-radius:50%;background:var(--sun);color:#1a1405;font-weight:600;font-size:13px;display:grid;place-items:center;font-variant-numeric:tabular-nums}
.legend .n.o{background:var(--accent);color:var(--surface)}
.legend small{display:block;color:var(--muted);font-size:12.5px}
.map-label{font-family:var(--body);font-size:11px;letter-spacing:.12em;text-transform:uppercase;fill:var(--muted);font-weight:600}
.pin-num{font-family:var(--body);font-size:12px;font-weight:600;fill:#1a1405}
.pin-num.o{fill:var(--surface)}
.pin-tag{font-family:var(--body);font-size:12.5px;font-weight:500;fill:var(--fg)}
.pin-tag.o{fill:var(--accent)}
.rank-head{margin:48px 0 10px}
.rank-head h2{font-family:var(--display);font-weight:400;font-size:36px;margin:0 0 6px;line-height:1.1}
.rank-head p{margin:0;color:var(--muted);max-width:66ch}
.options{display:grid;gap:22px;margin-top:18px}
.opt{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:22px;display:grid;grid-template-columns:200px minmax(0,1fr);gap:20px 26px}
.opt.top{border-color:var(--sun)}
.side{display:flex;flex-direction:column;gap:12px;min-width:0}
.mini{border-radius:10px;overflow:hidden;border:1px solid var(--line)}
.mini svg{display:block;width:100%;height:auto;background:var(--ocean)}
.badge{display:inline-flex;align-items:center;gap:8px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600;color:var(--muted)}
.badge .n{width:28px;height:28px;border-radius:50%;background:var(--sun);color:#1a1405;font-size:14px;display:grid;place-items:center;letter-spacing:0}
.where{font-size:13.5px;color:var(--muted);line-height:1.45}
.where b{color:var(--fg);font-weight:500}
.main{min-width:0;display:flex;flex-direction:column;gap:16px}
.opt h3{font-family:var(--display);font-weight:400;font-size:32px;line-height:1.05;margin:0;text-wrap:balance}
.opt h3 span{display:block;font-family:var(--body);font-size:15px;color:var(--muted);margin-top:6px}
.dates{font-size:13px;color:var(--muted);font-weight:500}
.dates b{color:var(--fg);font-weight:600}
.nums{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px}
.num{background:var(--bg);border-radius:10px;padding:10px 12px;min-width:0}
.num.hero{background:var(--sun-soft);outline:1px solid var(--sun)}
.num .l{font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600}
.num .v{font-family:var(--display);font-size:26px;line-height:1.1;margin-top:2px;font-variant-numeric:tabular-nums}
.num.hero .v{color:var(--sun)}
.num .s{font-size:12.5px;color:var(--muted);margin-top:2px}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-size:13px;padding:4px 10px;border-radius:999px;background:var(--accent-soft);color:var(--accent);font-weight:500}
.chip.warn{background:var(--sun-soft);color:var(--sun)}
.take{margin:0;font-size:15.5px;max-width:72ch}
.take b{font-weight:600}
.pc{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px 22px}
.pc h4{margin:0 0 6px;font-size:12px;letter-spacing:.12em;text-transform:uppercase;font-weight:600}
.pc h4.g{color:var(--good)} .pc h4.b{color:var(--bad)}
.pc ul{margin:0;padding:0;list-style:none;display:grid;gap:5px;font-size:14.5px}
.pc li{padding-left:18px;position:relative}
.pc li::before{content:"";position:absolute;left:0;top:.62em;width:8px;height:8px;border-radius:50%}
.pc .g + ul li::before{background:var(--good)} .pc .b + ul li::before{background:var(--bad)}
.links{display:flex;flex-wrap:wrap;gap:10px;padding-top:4px}
.btn{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:10px;text-decoration:none;font-weight:600;font-size:14.5px;border:1px solid var(--accent);color:var(--accent);background:transparent}
.btn.fill{background:var(--accent);color:var(--surface)}
.btn svg{width:16px;height:16px;flex:none}
@media (max-width:640px){
  .opt{grid-template-columns:1fr;padding:18px}
  .side{flex-direction:row;flex-wrap:wrap;align-items:flex-start}
  .side .mini{flex:0 0 150px}
  .side .meta{flex:1 1 160px;display:flex;flex-direction:column;gap:10px}
  .opt h3{font-size:28px}
}
@media (min-width:641px){ .side .meta{display:contents} }
.notes{margin-top:44px;padding-top:22px;border-top:1px solid var(--line);display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px 36px}
.notes h3{font-family:var(--display);font-weight:400;font-size:24px;margin:0 0 6px}
.notes ul{margin:0;padding-left:18px;font-size:14.5px;color:var(--muted);display:grid;gap:5px}
.notes li b{color:var(--fg);font-weight:500}
@media (prefers-reduced-motion: no-preference){
  .pulse{animation:pulse 2.4s ease-out infinite;transform-origin:center;transform-box:fill-box}
  @keyframes pulse{0%{transform:scale(.6);opacity:.7}100%{transform:scale(2.2);opacity:0}}
}
"""

JS_GEO = r"""
  var MEXICO_CA=[[-117.1,32.5],[-114.8,32.5],[-111,31.3],[-108.2,31.3],[-106.5,31.8],[-104.5,29.6],[-103,29],[-101.4,29.8],[-99.5,27.5],[-97.4,25.9],[-97.7,24],[-97.8,22.3],[-97.3,21],[-96.4,19.5],[-95.5,18.7],[-94.5,18.2],[-92.5,18.6],[-91.5,18.8],[-90.4,19.6],[-90.4,21.0],[-89.5,21.3],[-88.2,21.5],[-86.8,21.2],[-87.4,20.3],[-87.5,19.6],[-87.8,18.5],[-88.2,17.5],[-88.3,16.3],[-88.6,15.8],[-88.2,15.7],[-86.4,15.8],[-85.9,16.0],[-84.3,15.8],[-83.2,15.0],[-83.5,13.5],[-83.7,12.0],[-83.8,10.9],[-82.9,9.6],[-82.2,9.2],[-80.9,9.0],[-79.5,9.4],[-78.4,9.5],[-77.4,8.7],[-77.9,7.3],[-78.4,7.5],[-79.5,8.9],[-80.0,7.5],[-80.4,7.2],[-80.9,7.3],[-81.0,7.8],[-81.7,8.0],[-82.9,8.3],[-83.3,8.4],[-83.7,9.0],[-84.7,9.6],[-84.9,9.9],[-85.0,10.2],[-85.7,9.9],[-85.9,10.2],[-85.9,10.6],[-85.7,11.1],[-86.0,11.3],[-86.7,12.1],[-87.4,12.9],[-87.9,13.2],[-89.3,13.5],[-90.1,13.7],[-91.7,14.0],[-92.3,14.6],[-94.0,16.1],[-95.2,16.2],[-97.0,15.7],[-98.7,16.3],[-99.9,16.8],[-101.5,17.6],[-102.2,17.95],[-103.7,18.5],[-104.9,19.5],[-105.3,20.5],[-105.3,20.7],[-105.5,21.0],[-105.3,21.5],[-105.6,22.5],[-106.4,23.2],[-107.5,24.5],[-108.5,25.5],[-109.4,26.5],[-110.7,27.8],[-111.2,28.6],[-112.4,29.6],[-113.5,31.0],[-114.7,31.8],[-114.9,31.3],[-114.3,30.0],[-113.1,28.6],[-112.2,27.5],[-111.7,26.9],[-111.0,25.8],[-110.7,24.3],[-110.0,23.5],[-109.7,23.1],[-109.9,22.9],[-110.3,23.3],[-111.2,24.3],[-112.0,25.0],[-112.3,26.0],[-113.3,27.0],[-114.2,27.6],[-114.5,28.5],[-115.7,29.6],[-116.6,31.3]];
  var USA=[[-117.1,32.5],[-114.8,32.5],[-111,31.3],[-108.2,31.3],[-106.5,31.8],[-104.5,29.6],[-103,29],[-101.4,29.8],[-99.5,27.5],[-97.4,25.9],[-97.2,27.8],[-95.0,29.3],[-93.8,29.7],[-91.5,29.2],[-89.4,29.0],[-89.0,30.3],[-87.5,30.4],[-85.0,29.7],[-83.0,29.0],[-82.7,27.8],[-81.8,26.4],[-81.1,25.2],[-80.4,25.2],[-80.1,26.5],[-80.5,28.5],[-81.4,30.4],[-81.0,31.9],[-79.8,32.8],[-78.5,33.9],[-75.5,35.2],[-76.0,37.0],[-74.0,40.5],[-70.0,42.0],[-70.0,44.0],[-125,44.0],[-124.2,42],[-124.4,40.4],[-122.5,37.5],[-120.6,34.5],[-118.5,34],[-117.1,32.5]];
  var CUBA=[[-84.9,21.85],[-84.0,22.6],[-82.5,23.1],[-81.0,23.1],[-79.5,22.6],[-77.8,21.9],[-76.3,21.2],[-75.5,20.7],[-74.2,20.3],[-74.8,19.9],[-76.0,19.95],[-77.7,19.85],[-77.4,20.6],[-78.5,21.1],[-80.0,21.8],[-81.5,21.9],[-82.3,21.6],[-84.0,21.6]];
  var HISP=[[-74.4,18.6],[-73.4,19.9],[-72.0,19.7],[-70.5,19.85],[-69.8,19.4],[-69.2,19.3],[-68.4,18.6],[-68.8,18.35],[-69.9,18.4],[-71.1,17.6],[-71.7,17.9],[-72.8,18.2],[-74.2,18.3]];
  var JAM=[[-78.35,18.4],[-77.9,18.5],[-77.0,18.4],[-76.3,18.0],[-76.9,17.85],[-77.7,17.9],[-78.2,18.2]];
  var PR=[[-67.25,18.4],[-66.0,18.5],[-65.6,18.3],[-65.7,18.0],[-66.5,17.95],[-67.2,18.0]];
  var SAM=[[-77.4,8.7],[-76.9,8.5],[-76.2,9.3],[-75.6,10.3],[-75.5,10.6],[-74.9,11.1],[-74.2,11.3],[-73.3,11.3],[-72.3,11.8],[-71.3,12.3],[-71.6,10.8],[-70.2,11.6],[-69.0,11.5],[-68.3,10.6],[-66.9,10.6],[-65.0,10.1],[-63.0,10.7],[-61.9,10.7],[-60.6,8.5],[-60.6,4.0],[-78.5,4.0],[-78.0,7.0],[-77.9,7.3]];
  var LAND=[USA,MEXICO_CA,CUBA,HISP,JAM,PR,SAM];
  var ISLETS=[[-78.0,26.6],[-77.9,24.5],[-76.3,25.1],[-75.6,24.4],[-76.6,23.6],[-70.0,12.5],[-69.0,12.2],[-61.5,15.5],[-61.0,14.0],[-72.2,21.8],[-86.5,16.35]];
"""

def render(page, fname):
    opts_json = json.dumps(page['options'], ensure_ascii=False)
    tags_json = json.dumps(page['tags'], ensure_ascii=False)
    brief = ''.join(f'<span>{b}</span>' for b in page['brief'])
    def notes(block):
        return f"<div><h3>{block['h']}</h3><ul>" + ''.join(f'<li>{i}</li>' for i in block['items']) + '</ul></div>'
    out = f"""<title>{page['title']}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Instrument+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>

<div class="wrap">
  <div class="eyebrow">{page['eyebrow']}</div>
  <h1>{page['h1']}</h1>
  <div class="brief">{brief}</div>
  <p class="lede">{page['lede']}</p>

  <section class="map-card" aria-labelledby="mapTitle">
    <div class="map-head">
      <h2 id="mapTitle">Where they are</h2>
      <p>{page['map_sub']}</p>
    </div>
    <div id="mainMap"></div>
    <div class="legend" id="legend"></div>
  </section>

  <div class="rank-head">
    <h2>{page['rank_h2']}</h2>
    <p>{page['rank_p']}</p>
  </div>
  <div class="options" id="options"></div>

  <section class="notes">
    {notes(page['notes_a'])}
    {notes(page['notes_b'])}
    {notes(page['notes_c'])}
  </section>
</div>

<script>
(function(){{
{JS_GEO}
  var LON0=-125,LON1=-59,LAT0=6,LAT1=44,W=1000;
  var YS=1.08; var H=Math.round(W*(LAT1-LAT0)/(LON1-LON0)*YS);
  function P(ll){{return [ (ll[0]-LON0)/(LON1-LON0)*W, (LAT1-ll[1])/(LAT1-LAT0)*H ];}}
  function poly(pts){{return pts.map(function(p,i){{var q=P(p);return (i?'L':'M')+q[0].toFixed(1)+' '+q[1].toFixed(1);}}).join('')+'Z';}}
  var SLC=[-111.98,40.79];
  var OPTS={opts_json};
  var TAGS={tags_json};

  function arcPath(a,b){{
    var p=P(a),q=P(b);var mx=(p[0]+q[0])/2,my=(p[1]+q[1])/2;
    var dx=q[0]-p[0],dy=q[1]-p[1];var len=Math.hypot(dx,dy)||1;
    var cx=mx - dy/len*len*0.22, cy=my + dx/len*len*0.22;
    return 'M'+p[0].toFixed(1)+' '+p[1].toFixed(1)+' Q'+cx.toFixed(1)+' '+cy.toFixed(1)+' '+q[0].toFixed(1)+' '+q[1].toFixed(1);
  }}
  function landSVG(){{
    var s='';
    LAND.forEach(function(pl){{s+='<path d="'+poly(pl)+'" fill="var(--land)" stroke="var(--land-line)" stroke-width="1" stroke-linejoin="round"/>';}});
    ISLETS.forEach(function(ll){{var q=P(ll);s+='<circle cx="'+q[0].toFixed(1)+'" cy="'+q[1].toFixed(1)+'" r="2.6" fill="var(--land)" stroke="var(--land-line)" stroke-width="1"/>';}});
    return s;
  }}
  function pinSVG(ll,label,cls,r,off){{
    var q=P(ll);r=r||12;off=off||[0,0];var x=q[0]+off[0],y=q[1]+off[1];
    var s='<g>';
    if(off[0]||off[1]) s+='<line x1="'+q[0].toFixed(1)+'" y1="'+q[1].toFixed(1)+'" x2="'+x.toFixed(1)+'" y2="'+y.toFixed(1)+'" stroke="var(--surface)" stroke-width="2"/>';
    s+='<circle cx="'+x.toFixed(1)+'" cy="'+y.toFixed(1)+'" r="'+r+'" fill="'+(cls==='o'?'var(--accent)':'var(--sun)')+'" stroke="var(--surface)" stroke-width="2.5"/>'+
      '<text class="pin-num '+(cls||'')+'" x="'+x.toFixed(1)+'" y="'+(y+4.5).toFixed(1)+'" text-anchor="middle">'+label+'</text></g>';
    return s;
  }}
  function tag(ll,text,dx,dy,cls,anchor){{var q=P(ll);return '<text class="pin-tag '+(cls||'')+'" x="'+(q[0]+dx).toFixed(1)+'" y="'+(q[1]+dy).toFixed(1)+'" text-anchor="'+(anchor||'start')+'">'+text+'</text>';}}
  function lbl(ll,text){{var q=P(ll);return '<text class="map-label" x="'+q[0].toFixed(1)+'" y="'+q[1].toFixed(1)+'" text-anchor="middle">'+text+'</text>';}}

  var main='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Map of Mexico, Central America and the Caribbean with the options pinned and flight arcs from Salt Lake City">';
  main+=landSVG();
  main+=lbl([-118,20],'Pacific Ocean')+lbl([-90,24.5],'Gulf of Mexico')+lbl([-75.5,15.6],'Caribbean Sea')+lbl([-102.5,25.5],'Mexico')+lbl([-100,37.5],'United States')+lbl([-73,7.2],'Colombia');
  var arcsDone={{}};
  OPTS.forEach(function(o){{
    var k=o.ll.join(',');
    if(arcsDone[k]) return; arcsDone[k]=1;
    main+='<path d="'+arcPath(SLC,o.ll)+'" fill="none" stroke="var(--arc)" stroke-width="1.6" opacity=".75"/>';
  }});
  var slcQ=P(SLC);
  main+='<circle class="pulse" cx="'+slcQ[0].toFixed(1)+'" cy="'+slcQ[1].toFixed(1)+'" r="9" fill="none" stroke="var(--accent)" stroke-width="2"/>';
  main+=pinSVG(SLC,'SLC','o',15)+tag(SLC,'Salt Lake City',20,5,'o');
  TAGS.forEach(function(t){{main+=tag(t.ll,t.text,t.dx,t.dy,'',t.anchor);}});
  OPTS.forEach(function(o){{main+=pinSVG(o.ll,String(o.n),'',12,o.off);}});
  main+='</svg>';
  document.getElementById('mainMap').innerHTML=main;

  var leg='<div><span class="n o">SLC</span><span>Salt Lake City<small>Where everyone departs</small></span></div>';
  OPTS.forEach(function(o){{leg+='<div><span class="n">'+o.n+'</span><span>'+o.name+'<small>'+o.place.split(',')[0]+' · '+o.couple+' for the couple</small></span></div>';}});
  document.getElementById('legend').innerHTML=leg;

  var pinIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 21h18M5 21V7l7-4 7 4v14M9 21v-6h6v6"/></svg>';
  var planeIcon='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 16l20-8-6 14-3-6-6-3z"/></svg>';
  var html='';
  OPTS.forEach(function(o){{
    var mini='<svg viewBox="0 0 '+W+' '+H+'" role="img" aria-label="Location of '+o.name+'">'+landSVG();
    mini+='<path d="'+arcPath(SLC,o.ll)+'" fill="none" stroke="var(--arc)" stroke-width="2.2" opacity=".8"/>';
    mini+=pinSVG(SLC,'','o',7);
    var q=P(o.ll);
    mini+='<circle cx="'+q[0].toFixed(1)+'" cy="'+q[1].toFixed(1)+'" r="34" fill="var(--sun)" opacity=".22"/>';
    mini+=pinSVG(o.ll,String(o.n),'',19);
    mini+='</svg>';
    var chips=o.chips.map(function(c){{return '<span class="chip">'+c+'</span>';}}).join('')+o.warn.map(function(c){{return '<span class="chip warn">'+c+'</span>';}}).join('');
    var fareSub=o.fareS+(o.nonstop?'. Nonstop '+o.nonstop+', '+o.nonstopS:'');
    var coupleSub='rental + 2 seats'+(o.extraS?', '+o.extraS:'')+(o.nonstop?'. '+o.coupleNS+' flying nonstop':'');
    html+='<article class="opt'+(o.n===1?' top':'')+'" id="option-'+o.n+'">'+
      '<div class="side"><div class="mini">'+mini+'</div><div class="meta">'+
        '<span class="badge"><span class="n">'+o.n+'</span>'+(o.n===1?'Lowest bill':'Rank '+o.n)+'</span>'+
        '<div class="where"><b>'+o.place+'</b><br>'+o.apt+'</div></div></div>'+
      '<div class="main">'+
        '<h3>'+o.name+'<span>'+o.sub+'</span></h3>'+
        '<div class="dates">Priced for <b>'+o.dates+'</b></div>'+
        '<div class="nums">'+
          '<div class="num hero"><div class="l">Couple\\'s total</div><div class="v">'+o.couple+'</div><div class="s">'+coupleSub+'</div></div>'+
          '<div class="num"><div class="l">Rental, 3 nights</div><div class="v">'+o.rental+'</div><div class="s">before local tax</div></div>'+
          '<div class="num"><div class="l">Per night</div><div class="v">'+o.night+'</div><div class="s">whole property</div></div>'+
          '<div class="num"><div class="l">Flight, per person</div><div class="v">'+o.fare+'</div><div class="s">'+fareSub+'</div></div>'+
        '</div>'+
        '<div class="chips">'+chips+'</div>'+
        '<p class="take">'+o.take+'</p>'+
        '<div class="pc"><div><h4 class="g">Pros</h4><ul>'+o.pros.map(function(x){{return '<li>'+x+'</li>';}}).join('')+'</ul></div>'+
        '<div><h4 class="b">Cons</h4><ul>'+o.cons.map(function(x){{return '<li>'+x+'</li>';}}).join('')+'</ul></div></div>'+
        '<div class="links"><a class="btn fill" href="'+o.air+'" target="_blank" rel="noopener">'+pinIcon+'Open the Airbnb listing</a>'+
        '<a class="btn" href="'+o.fly+'" target="_blank" rel="noopener">'+planeIcon+'Flights on Google Flights</a>'+
        (o.flyNS?'<a class="btn" href="'+o.flyNS+'" target="_blank" rel="noopener">'+planeIcon+'Nonstop only</a>':'')+'</div>'+
      '</div></article>';
  }});
  document.getElementById('options').innerHTML=html;
}})();
</script>
"""
    open(OUT + fname, 'w').write(out)
    print(fname, len(out), 'bytes')
    for o in page['options']:
        print(f"  {o['n']} {o['name']}: {o['dates']} rental {o['rental']} fare {o['fare']} couple {o['couple']}" + (f" (nonstop {o['coupleNS']})" if 'coupleNS' in o else ''))

render(MAR, 'beach-wedding-shortlist.html')
render(JAN, 'january-beach-wedding.html')
