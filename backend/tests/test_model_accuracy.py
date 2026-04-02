import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# =====================================================
# CONFIG
# =====================================================

BASE_URL = "http://127.0.0.1:8000"
REGISTER_URL = f"{BASE_URL}/auth/register"
LOGIN_URL = f"{BASE_URL}/auth/login"
ASK_URL = f"{BASE_URL}/recommendation/ask"

TEST_USER = {
    "username": "accuracy_user",
 "email": "aaa@gamil.com",
    "password": "Aa1!1234"
}

# =====================================================
# AUTHENTICATION (AUTO LOGIN)
# =====================================================

def get_token():
    # Register (ignore if already exists)
    requests.post(REGISTER_URL, json={
        "username": TEST_USER["username"],
        "email": TEST_USER["email"],
        "confirm_email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })

    # Login to obtain JWT token
    response = requests.post(LOGIN_URL, json={
        "email": TEST_USER["email"],
        "password": TEST_USER["password"]
    })

    if response.status_code != 200:
        raise Exception("Login failed: " + response.text)

    return response.json()["access_token"]


# =====================================================
# TEST DATA (SAMPLES)
# =====================================================

test_cases = [

#01
    {
        "question": "How much money do I need to begin minimum investing in Sri Lanka’s share market?",
        "expected": """As a financial advisor, I'd be happy to guide you on the minimum investment requirements for Sri Lanka's share market. 

**Understanding the Basics**

To begin investing in Sri Lanka's share market, you'll need to open a trading account with a licensed stockbroker. The minimum investment amount varies depending on the broker and the type of account you choose.

**Minimum Investment Requirements**

Typically, the minimum investment requirements for a trading account in Sri Lanka are:

- For a basic trading account: LKR 10,000 (approximately USD 45) to LKR 50,000 (approximately USD 225)
- For a margin trading account: LKR 100,000 (approximately USD 450) to LKR 500,000 (approximately USD 2,250)

**Allocation Plan**

Assuming you're a beginner, I recommend starting with a basic trading account and allocating 10% to 20% of your investment towards Sri Lanka's share market. This will help you gain experience and diversify your portfolio.

For example, if you have LKR 100,000 (approximately USD 450) to invest, consider allocating:

- LKR 10,000 (approximately USD 45) to LKR 20,000 (approximately USD 90) to Sri Lanka's share market
- The remaining amount to other investment options, such as fixed deposits, bonds, or mutual funds.

**Next Steps**

Before investing, ensure you:

- Research and understand the risks associated with share market investments
- Set clear financial goals and risk tolerance
- Consult with a financial advisor (like me) to create a personalized investment plan

Remember, investing in the share market involves risks, and it's essential to educate yourself
"""
    },
    
    #02
    {
        "question": "Should I sell Rs.5,000 in DIAL as a starting investment?",
        "expected": """n 2026, selling Rs. 5,000 in Dialog Axiata PLC (DIAL) depends on your financial goal, as the stock is currently performing strongly but is viewed by some analysts as reaching a peak valuation. As of March 2, 2026, the share price is approximately Rs. 34.50. 
A holding of Rs. 5,000 equates to roughly 144 shares.

Key Considerations for Your Decision
Strong Recent Performance: DIAL has seen a significant price surge, rising over 150% in the last year. This follows a robust FY 2025 where the group recorded a Rs. 20.8 billion profit, a 67% increase year-on-year.
Dividend Income: The Board recently proposed a dividend of Rs. 1.50 per share for FY 2025. If you hold these shares until the "Ex-Dividend" date (expected mid-2026), you would receive approximately Rs. 216 in passive income.
Analyst Outlook: While some technical indicators like the RSI (74.95) suggest the stock is in "overbought" territory, consensus targets vary. Some analysts estimate a fair value around Rs. 38–42, while others warn of a potential correction toward Rs. 21.85.
Transaction Costs: Selling Rs. 5,000 will incur a total transaction fee of 1.12% (approx. Rs. 56). 
Dialog
Dialog
 +7
Summary Recommendation
Hold: If you are a long-term investor looking for steady dividends and exposure to Sri Lanka's growing 5G infrastructure (Dialog plans a USD 100 million expansion over the next two years).
Sell: If you have achieved a specific profit target and wish to reallocate capital into other sectors. The market is currently shifting into a "selective phase" where broad-based gains may slow down. 
Dialog
Dialog
 +1
Note: For such a small amount, the impact of brokerage fees is minimal, but frequent trading of small sums can erode your capital over time. Ensure your next investment has a clear entry and exit strategy.

"""
    },

#03
    {
        "question": "I prefer low-risk investments — what stocks should I consider?",
        "expected": """For a low-risk approach in Sri Lanka’s share market in 2026, you should focus on Defensive Stocks and Blue-Chip Companies. These entities typically provide essential services (food, fuel, banking), maintain stable earnings regardless of the economic cycle, and have a strong track record of paying regular dividends. 

Top Low-Risk Stock Categories (2026)
Established Blue Chips: These are the largest, most stable companies on the Colombo Stock Exchange (CSE).
John Keells Holdings (JKH): A diversified conglomerate with interests in real estate, retail, and logistics. It is highly regarded for its governance and consistent performance.
Commercial Bank of Ceylon (COMB): A leading private bank with a significant market share and a history of reliable dividend payments.
Hemas Holdings (HHL): Operates in defensive sectors like healthcare and consumer goods (FMCG), which tend to remain stable during downturns.
High-Yield Defensive Stocks: Companies in sectors with steady demand often offer attractive dividends.
Ceylon Tobacco Company (CTC): Known for exceptionally high dividend yields (approx. 8.9%) and stable demand for its products.
Chevron Lubricants Lanka (LLUB): A consistent dividend payer in the energy minerals sector with a yield of roughly 7.8%.
Sampath Bank (SAMP): Currently showing a high dividend yield of 6.4% and a "Strong Buy" analyst rating in early 2026.
Utility & Essential Services:
Dialog Axiata (DIAL): The telecommunications leader with a dividend yield of 4.3% and continued growth potential from data and infrastructure expansion.
Ceylon Cold Stores (CCS): A key player in food and beverage with a solid dividend yield of 7.1%. 
Summary of Key Stable Stocks (March 2026)
Company 	Sector	Market Cap	Div Yield
Ceylon Tobacco (CTC)	Consumer Goods	Rs. 332.6 B	8.9%
Sampath Bank (SAMP)	Banking	Rs. 188.5 B	6.4%
Ceylon Cold Stores (CCS)	Food & Beverage	Rs. 106.7 B	7.1%
Dialog Axiata (DIAL)	Telecom	Rs. 317.4 B	4.3%
Commercial Bank (COMB)	Banking	Rs. 359.6 B	2.5%
Lower-Risk Alternatives
If individual stocks feel too volatile, consider these alternatives:
Treasury Bills & Bonds: Backed by the government, these are the lowest-risk investments in Sri Lanka. 12-month T-bill rates are projected to be around 8–8.5% in 2026.
Unit Trusts (Mutual Funds): Professional managers diversify your money across many stocks, reducing the risk of a single company failing. 
Facebook
Facebook
 +1
For real-time data, you can track these companies on the CSE Official Website or use the CSE Mobile App. Always consult with a licensed investment advisor before making significant financial commitments."""
    },
    
    #04
    {
        "question": "Is it better to invest all my capital in one stock or spread it across many?",
        "expected": """In 2026, the consensus among financial experts at the Colombo Stock Exchange (CSE) is that spreading your capital across many stocks (diversification) is significantly better for low-risk investors than investing in just one.

Why Spreading Capital is Better
Reduces "Company-Specific" Risk: If you invest only in one company and it faces a scandal, management failure, or a bad earnings report, you could lose a large portion of your money. Spreading funds ensures that a loss in one stock can be offset by gains in another.
Lower Volatility: Diversified portfolios in Sri Lanka have been shown to reduce overall price swings by up to 30% compared to single-stock holdings.
Protection Against Sector Shocks: Different sectors react differently to economic changes. For example, while tourism might struggle during a global travel slump, essential services like telecommunications or food retail often remain stable.

Recommended Number of Stocks (2026)
For a beginner or low-risk investor in the CSE, the following guidelines are recommended:
Starting Out: Aim for 3 to 5 solid stocks from different sectors (e.g., one banking, one telecom, one consumer goods).
Growth Phase: As your capital grows, a well-balanced portfolio typically holds 8 to 12 stocks.
The "5% Rule": Many advisors suggest never putting more than 5–10% of your total investment into a single company.

A Low-Risk "Middle Ground"
If managing multiple individual stocks feels overwhelming or too expensive due to transaction fees, consider Unit Trusts (Mutual Funds). 

Instant Diversification: One small investment (often starting at Rs. 1,000) gives you exposure to a professional basket of 20+ stocks.
Expert Management: Professional fund managers at firms like CAL or NDB Wealth rebalance the portfolio for you to keep risk low. 

Verdict: For your low-risk preference, never invest all your capital in one stock. Start by spreading your money across at least 3–5 high-quality "Blue Chip" companies or a diversified Unit Trust to protect your savings. 

"""
    },
    
    #05
    {
        "question": "Should I start with equities or fixed-income instruments if I’m risk-averse?",
        "expected": """In 2026, the consensus among financial experts at the Colombo Stock Exchange (CSE) is that spreading your capital across many stocks (diversification) is significantly better for low-risk investors than investing in just one.

Why Spreading Capital is Better
Reduces "Company-Specific" Risk: If you invest only in one company and it faces a scandal, management failure, or a bad earnings report, you could lose a large portion of your money. Spreading funds ensures that a loss in one stock can be offset by gains in another.
Lower Volatility: Diversified portfolios in Sri Lanka have been shown to reduce overall price swings by up to 30% compared to single-stock holdings.
Protection Against Sector Shocks: Different sectors react differently to economic changes. For example, while tourism might struggle during a global travel slump, essential services like telecommunications or food retail often remain stable.

Recommended Number of Stocks (2026)
For a beginner or low-risk investor in the CSE, the following guidelines are recommended:
Starting Out: Aim for 3 to 5 solid stocks from different sectors (e.g., one banking, one telecom, one consumer goods).
Growth Phase: As your capital grows, a well-balanced portfolio typically holds 8 to 12 stocks.
The "5% Rule": Many advisors suggest never putting more than 5–10% of your total investment into a single company.


A Low-Risk "Middle Ground"
If managing multiple individual stocks feels overwhelming or too expensive due to transaction fees, consider Unit Trusts (Mutual Funds). 

Instant Diversification: One small investment (often starting at Rs. 1,000) gives you exposure to a professional basket of 20+ stocks.
Expert Management: Professional fund managers at firms like CAL or NDB Wealth rebalance the portfolio for you to keep risk low. 

Verdict: For your low-risk preference, never invest all your capital in one stock. Start by spreading your money across at least 3–5 high-quality "Blue Chip" companies or a diversified Unit Trust to protect your savings. 


"""
    },

# 6
{
"question": "If I invest Rs.10,000 today, what strategy should I use?",
"expected": """With Rs. 10,000 and a risk-averse profile, your best strategy in 2026 is to avoid direct stock picking—where transaction fees and volatility can quickly eat into a small balance—and instead use Unit Trusts or Fixed Income instruments.
Recommended Strategy: The 80/20 Stability Split
Since you prefer low risk, allocate your Rs. 10,000 as follows:
Fixed Income Core (Rs. 8,000):
Investment: A Money Market Fund (Unit Trust).
Why: These funds invest in highly secure government Treasury Bills and bank deposits.
Top Option: The CAL Money Market Fund or NDB Wealth Money Fund are ideal. They offer yields around 7.5% – 8.2%, which is higher than standard savings accounts (approx. 2-4%).
Benefit: You can withdraw your money anytime without the penalties associated with traditional Fixed Deposits.
Equity Growth Explorer (Rs. 2,000):
Investment: An Equity Unit Trust or a Growth & Income Fund.
Why: Instead of buying just one stock like DIAL, this pools your Rs. 2,000 with other investors to own a tiny slice of 30+ major Sri Lankan companies (blue chips like JKH and Commercial Bank).
Top Option: NDB Wealth Growth & Income Fund (minimum Rs. 10,000 for some specific funds, but many CAL Unit Trusts allow entries as low as Rs. 100).

Why Not Direct Stocks?
For a small Rs. 10,000 investment:
Fees: A single "buy" and "sell" on the share market costs 1.12% per transaction.
Lack of Diversification: Rs. 10,000 isn't enough to build a diversified portfolio of 5-10 stocks. One bad month for a single company could wipe out your gains.
Inflation Protection: While Sri Lankan inflation is currently low (approx. 1.6% as of Feb 2026), it is projected to rise toward 5% later this year. A purely fixed-income approach might struggle to stay ahead, which is why the 20% equity "booster" is helpful.

Summary Plan (March 2026)
Open an Account: Register digitally with a Unit Trust manager like CAL or NDB Wealth.
Initial Deposit: Move your Rs. 10,000 into the Money Market Fund first to start earning daily interest immediately.
Automate: If you can, set up a Systematic Investment Plan (SIP) to add a small amount (e.g., Rs. 1,000) every month to build wealth through compounding. 


"""
},

# 7
{
"question": "How often should I check my investment performance?",

"expected": """In 2026, financial advisors recommend that low-risk investors check their investment performance once a month or once a quarter. Checking more frequently, such as daily, often leads to "myopic loss aversion," where you feel the emotional stress of short-term market "noise" more than the benefits of long-term gains. 

Recommended Review Schedule
The frequency of your check-ins should align with your specific investment types and goals:
Quarterly Reviews (Every 3 Months): This is the "sweet spot" for most long-term investors. It allows you to review performance against benchmarks without reacting to temporary volatility. This is also when Sri Lankan listed companies release their Interim Financial Statements, providing essential data for informed decision-making.
Monthly Check-ins: Suitable if you are actively contributing via a monthly Systematic Investment Plan (SIP) or are nearing retirement and need to manage cash flow.
Annual "Check-up": A comprehensive yearly review is necessary to ensure your portfolio still aligns with your life goals (e.g., marriage, home purchase) and to rebalance your asset allocation if one sector has grown too large. 

Why Less Frequent is Often Better
Factor 	Daily Checking	Monthly/Quarterly Checking
Emotional Impact	High stress; prone to panic selling.	Calmer; focused on long-term goals.
Decision Quality	Often reactive (buying high/selling low).	Strategic; based on fundamental trends.
Performance	Research shows frequent checkers take less risk and earn less.	Allows compounding to work effectively.
When to "Check-in" Early
While a fixed schedule is best, you should briefly reassess your portfolio outside of your normal routine if:
Significant Life Events occur (e.g., marriage, job change, or inheritance).
Market-Specific Triggers arise, such as a major company-specific crisis or a notification that an asset has dropped below a pre-set "stop-loss" threshold (e.g., the 7% rule). 

For low-risk investors in 2026, the best approach is to automate your investments (like monthly SIPs) and limit manual checks to once a month to maintain emotional discipline and support compound growth.

"""
},

# 8
{
"question": "What is a realistic return I can expect in a year?",

"expected": """In 2026, a realistic return for a low-risk investor in Sri Lanka ranges from 7.5% to 11% annually, depending on the specific asset class you choose. While the stock market has shown higher historical growth, fixed-income options currently offer a more predictable and secure return profile. 
Realistic Annual Return Targets (March 2026)
Fixed Income (Very Low Risk): You can realistically expect 7.6% to 8.5%.
Treasury Bills: As of February 27, 2026, 12-month T-bills were auctioned at an average yield of 8.24%.
Fixed Deposits (FDs): Major banks are offering 1-year FD rates between 8.00% and 8.50%.
Senior Citizen Schemes: These can yield significantly higher returns, up to 12.25% for longer-term 5-year deposits.
Unit Trusts (Low to Moderate Risk):
Money Market Funds: Typically target returns of 7.5% to 8.2%, consistently slightly outperforming standard bank savings rates with high liquidity.
Income Funds: These focus on corporate bonds and can provide a slight "premium" return of 8% to 10%.
Blue-Chip Dividend Stocks (Moderate Risk):
If you invest in stable, high-yielding companies, you can target 6.4% to 9% in dividends alone, plus potential capital appreciation. For example, Ceylon Tobacco (CTC) and Watawala Plantations (WATA) currently show dividend yields of approximately 8.7% to 9.7%. 

Real Return vs. Inflation
To understand your actual wealth growth, you must consider inflation.
Inflation Forecast: Sri Lanka's headline inflation is projected to stay below the Central Bank's 5% target, likely averaging around 4.1% for 2026.
Net Gain: If you earn 8.24% from a T-bill while inflation is at 4.1%, your "real" return (purchasing power increase) is approximately 4.14%. 

Summary of Returns by Investment Type
Investment Type 	Expected Annual Return	Risk Level
Savings Accounts	2.5% – 3.5%	Lowest
Money Market Funds	7.5% – 8.2%	Very Low
12-Month Treasury Bills	8.24%	Very Low
1-Year Fixed Deposits	8.00% – 8.50%	Low
Blue-Chip Dividends	6.4% – 9.7%	Moderate
Stock Market (ASPI)	10% – 15% (Historic Avg)	High
Recommendation: For a risk-averse beginner, aiming for 8% is highly realistic in the current 2026 environment. You can achieve this securely through 12-month Treasury Bills or a reputable Money Market Fund. 
"""
},

# 9
{
"question": "What are the challenges SMEs face when seeking investment in Sri Lanka?",
"expected": """In 2026, Small and Medium Enterprises (SMEs) in Sri Lanka—which contribute over 52% of the national GDP—face a significant "financing gap" despite recent government efforts to stabilize the economy. While the 2026 National Budget introduced measures like lower tax investment thresholds and concessional loans, structural and operational barriers remain the primary challenges for SMEs seeking investment. 
1. Financial & Lending Barriers
The most critical challenge is the difficulty in accessing traditional bank credit, which remains the primary source of capital for most local firms. 
Collateral Requirements: Banks frequently demand heavy collateral, often exceeding the value of the loan itself. Many SMEs, particularly startups or those in the service sector, lack fixed assets like land or buildings to secure these funds.
High Interest Rates: Although rates have eased from 2022 peaks, SMEs still face commercial lending rates ranging from 10% to 27%, making long-term borrowing unattractive and eroding profit margins.
Stringent Approval Processes: Lengthy and bureaucratic approval cycles often result in funds arriving too late to capitalize on market opportunities. 
2. Operational & Capacity Constraints
Many SMEs struggle to meet the professional standards required by international or large-scale domestic investors. 

Inadequate Record-Keeping: A lack of audited financial statements and a tendency to mix personal and business finances make many SMEs "unbankable" in the eyes of commercial lenders.
Skills & Knowledge Gaps: There is a notable shortage of competent specialists to help SMEs implement modern financial reporting standards (like IFRS for SMEs) or navigate complex digital transitions.
Technological Lag: Many businesses lack the digital infrastructure or AI-driven tools necessary to compete in a tech-driven global economy, which discourages venture capital (VC) investment focused on scalability. 

3. Policy & Structural Issues
External factors at the national level continue to create an unpredictable environment for investors. 
Regulatory Uncertainty: Frequent shifts in government policy and tax frameworks (such as the recent VAT base expansion to lower thresholds) create uncertainty that discourages long-term investment.
Underdeveloped Ecosystem: While growing, the local "alternative finance" scene—including angel investors and impact funds—is still relatively small and often favors a few high-profile tech startups over the broader SME majority.
Market Size: Sri Lanka’s domestic market is relatively small (22 million people), and many SMEs lack the international networks or export certifications needed to scale globally. 
2026 Mitigation Efforts
To address these gaps, the government has launched several 2026 initiatives:
National Credit Guarantee Institution (NCGI): Plans to issue Rs. 7 billion in credit guarantees in 2026 to unlock Rs. 10 billion in lending, specifically targeting SMEs without collateral.
Concessional Loans: Specific schemes like the NCRCS (Sarusara) offer agricultural loans up to Rs. 3 million at 5% interest.
Agni Fund: A dedicated USD 5 million initiative launched in 2026 to support early-stage startups and innovation-driven enterprises. 

"""
},

# 10
{
"question": "What role will inflation and interest rates play in shaping investor confidence in Sri Lanka?",
"expected": """In 2026, inflation and interest rates act as the primary "anchors" for investor confidence in Sri Lanka, shifting the focus from crisis recovery to long-term stability. As of March 2026, these factors are shaping a cautiously optimistic environment. 
1. Inflation: The Stability Anchor
Inflation is currently the strongest driver of confidence, as it remains exceptionally low compared to the historic highs of 2022. 
Current Status: Annual inflation in Colombo slowed to 1.6% in February 2026, down from 2.3% in January.
Target Alignment: The Central Bank of Sri Lanka (CBSL) is guiding inflation toward a 5% target by mid-2026.
Investor Impact: Low inflation preserves the "real" value of returns. For instance, an 8% return on a Treasury bill currently yields a healthy ~6.4% profit after accounting for 1.6% inflation, which keeps investors interested in fixed-income assets. 

2. Interest Rates: The Valuation Driver
Interest rates are currently in a "hold" phase, providing a predictable backdrop for corporate planning and stock market valuations. 
Policy Stance: The CBSL has maintained the Overnight Policy Rate (OPR) at 7.75% throughout early 2026 to support continued economic growth.
Market Yields: 12-month Treasury bill yields are projected to stay within the 8.0%–8.5% range.
Investor Impact:
Equities: Stable, low rates make borrowing cheaper for companies, boosting profits and supporting higher stock market valuations.
Fixed Income: While yields are lower than in previous years, they are still considered attractive for risk-averse investors due to the current low-inflation environment. 

3. Emerging Challenges to Confidence
Despite the current stability, investors are watching for "undercurrents of concern" that could affect medium-term confidence: 
Liquidity Pressures: Rising private sector credit (expected to grow 18% in 2026) is putting pressure on banking sector liquidity, which could nudge market interest rates upward later in the year.
External Risks: Global uncertainties, such as potential US trade tariffs (up to 20–30% for Sri Lanka), are viewed as significant growth headwinds that could force the Central Bank to adjust rates to protect the economy.
Supply Shocks: Recent events like Cyclone Ditwah caused temporary spikes in food prices, reminding investors that inflation remains vulnerable to weather-related disruptions. 

Summary of Market Sentiment (March 2026)
Factor 	Current Trend	Impact on Confidence
Inflation	Decelerating (1.6%)	Positive — Increases real returns.
Policy Rates	Stable (7.75%)	Positive — Supports corporate growth.
G-Sec Yields	Rising Trend (8-8.5%)	Mixed — Benefits savers; pressures stock prices.
Medium-term	Weakening Perception	Caution — Driven by domestic macroeconomic risks.
Given this environment, would you like to explore specific investment sectors that typically outperform when inflation is low and interest rates are stable?"""
},

# 11
{
"question": "Future outlook for JKH (John Keells Holdings)",
"expected": """The future outlook for John Keells Holdings PLC (JKH) in 2026 is bullish, characterized by a significant earnings turnaround as its multi-billion dollar mega-projects transition from the construction phase to operational profitability. Analysts forecast a massive 168.7% year-on-year jump in net profit for FY2026, reaching an estimated Rs. 14.3 billion. 

Key Growth Drivers for 2026
City of Dreams Sri Lanka (CoDSL): The $1.2 billion integrated resort is the primary catalyst. After the October 2024 launch of the Cinnamon Life hotel, the second phase—including the casino, the ultra-luxury Nuwa hotel, and a mall—is scheduled to be operational by August 2, 2025. The project recorded its first positive EBITDA of Rs. 1.43 billion in late FY2026.
West Container Terminal (WCT): Phase I is already performing ahead of expectations, handling over 360,000 TEUs in Q3 FY2026. Full terminal completion is scheduled for mid-2026, which is expected to significantly boost transportation sector margins.
New Energy Vehicle (NEV) Business: The partnership with BYD has seen high demand, with an order book exceeding 3,900 vehicles as of early 2026. Analysts expect this segment to become a major EBIT contributor by FY2027.
Banking Sector Expansion: JKH’s banking arm, Nations Trust Bank (NTB), is expected to complete its acquisition of HSBC’s retail banking business in Sri Lanka during the first half of 2026. 

Analyst Valuations & Performance
As of March 2, 2026, the stock is trading around Rs. 22.10 – 22.40. Analysts maintain a "Maintain Buy" rating with the following targets: 

FY2026 Target Price: Rs. 27.00.
FY2027 Target Price: Rs. 34.00.
Dividends: JKH declared a second interim dividend of Rs. 0.10 per share for FY2026 in January 2026, signaling confidence in cash flow. 

Key Risks to Watch
Debt Servicing: High interest costs and depreciation linked to City of Dreams initially impacted net margins (currently ~2%), though these are expected to normalize as revenue ramps up.
External Factors: Ongoing volatility in global shipping routes (Red Sea crisis) and domestic recovery from weather-related supply shocks (e.g., Cyclone Ditwah) may cause short-term fluctuations in the transportation and consumer sectors. 
"""
},

# 12
{
"question": "Is JKH a safe investment for risk-averse investors?",
"expected": """In 2026, John Keells Holdings (JKH) is considered a low-to-moderate risk investment. While its status as Sri Lanka’s premier blue-chip company and its high credit rating provide significant safety, it is currently in a high-growth phase that introduces more volatility than a traditional "safe" asset like a Treasury bill. 
Why JKH is Considered "Safe" (Low Risk Factors)
Highest Credit Rating: JKH maintains a National Long-Term Rating of 'AAA(lka)' with a stable outlook from Fitch Ratings, indicating the lowest level of default risk in Sri Lanka.
Strong Balance Sheet: The company has a satisfactory net debt-to-equity ratio of 28% and an interest coverage ratio of 8.1x, meaning it easily generates enough profit to pay interest on its loans.
Reliable Dividends: JKH has a consistent history of paying dividends twice a year. In early 2026, it paid an interim dividend of Rs. 0.10 per share, with a total annual dividend yield typically around 1.1% to 2.1%.
Diversification: Because JKH operates in transportation, retail, leisure, and banking, a downturn in one sector is often offset by stability in another. 

Risks for the Risk-Averse (Volatility Factors)
Price Volatility: As a major market mover, JKH's share price can fluctuate significantly with market sentiment. In early 2026, it has traded between Rs. 18 and Rs. 26, meaning short-term capital losses are possible.
Large-Scale Project Risk: The $1.2 billion "City of Dreams" project is a massive undertaking. While it is now generating positive EBITDA, any delays in full operational ramp-up can impact short-term earnings.
Foreign Exchange Exposure: Approximately 55% of JKH’s total debt is denominated in foreign currency (mainly USD), making its profits sensitive to any sudden devaluation of the Sri Lankan Rupee. 

Summary for Risk-Averse Investors
Feature 	Assessment	Risk Level
Capital Preservation	Strong 'AAA' rating and solid assets.	Low
Income Stability	Consistent but modest dividend yield.	Low
Price Stability	Can experience 10-20% swings in a year.	Moderate
Growth Potential	High, driven by mega-projects and BYD.	N/A (Benefit)
Verdict: If your goal is absolute safety (zero chance of losing principal), you should stick to Treasury Bills. If you are comfortable with moderate price swings in exchange for potential long-term growth and a 'AAA' security profile, JKH is one of the safest equity investments in Sri Lanka for 2026.
"""
},

# 13
{
"question": "Future prediction for COMB (Commercial Bank of Ceylon)",
"expected": """The future outlook for Commercial Bank of Ceylon (COMB) in 2026 is bullish, supported by record-breaking loan growth and a significant recovery in net interest income. As the first private sector bank in Sri Lanka to cross the Rs. 2 trillion loan book milestone in 2025, COMB is well-positioned to capitalize on the country's economic resurgence. Analysts maintain a "Maintain Buy" recommendation with target prices for the voting share (COMB.N) reaching up to Rs. 225.00 by the end of 2026. 

Financial Performance & Forecasts
Earnings Growth: Net profit is forecast to reach Rs. 70.6 billion in 2026, up from an estimated Rs. 62.9 billion in 2025.
Net Interest Income (NII): NII grew by 18.97% to Rs. 136.29 billion in 2025. While lower market rates may compress margins, continued credit expansion—which averaged Rs. 45 billion per month in 2025—is expected to offset this impact.
Asset Quality: The bank’s impairment charges fell by over 73% YoY in late 2025 due to the absence of heavy provisioning for sovereign bonds. Its Stage 3 loan ratio improved significantly to 1.8%. 

Key Metrics & Targets (March 2026)
Metric 	2026 Forecast / Target	Status (as of March 2026)
Share Price (COMB.N)	Rs. 225.00	Rs. 221.50 (Feb 27, 2026)
Net Profit	Rs. 70.6 Billion	Upward Trend
Dividend Yield	5.3% - 5.5%	Solid Coverage
ROE	17.2% - 18.0%	Industry Leading
Dividends and Shareholder Value
COMB remains a reliable dividend payer. A final dividend for FY2025 is scheduled with an Ex-Dividend (XD) date of April 2, 2026, and payment on April 24, 2026. Analysts project an annual dividend amount of Rs. 12.20 per share for 2026. 

Strategic Risks
SME Exposure: As the largest lender to the SME sector, COMB faces potential impairment risks from localized economic shocks, such as the impact of Cyclone Ditwah on smaller businesses.
Margin Compression: The Central Bank's pressure to reduce lending rates may lead to a moderation in Net Interest Margins (NIMs) in the near term. 

For the latest official disclosures, visit the Commercial Bank Investor Relations page or the CSE Company Profile."""
},

# 14
{
"question": "Is DIAL (Dialog Axiata) a good choice for low-risk investors?",
"expected": """In 2026, Dialog Axiata PLC (DIAL) is considered a strong choice for low-risk investors due to its market-leading position, stable financial performance, and highest-possible credit rating. While all equities carry market risk, DIAL’s defensive nature as a utility-like service provider makes it one of the most stable stocks on the Colombo Stock Exchange (CSE). 
Why DIAL is Suitable for Low-Risk Investors
Top-Tier Credit Rating: DIAL holds a 'AAA(lka)' National Long-Term Rating from Fitch Ratings with a stable outlook, the highest rating on the Sri Lankan scale. This indicates a very low risk of default and high financial reliability.
Strong 2025 Performance: For the financial year ended December 31, 2025, the company reported a net profit of Rs. 20.8 billion, representing a 67% increase year-on-year.
Consistent Dividend Payer: The Board has recommended a dividend of Rs. 1.50 per share for FY 2025, offering a dividend yield of approximately 5.0%. DIAL typically maintains a policy of paying out roughly 50–60% of its net income as dividends.
Dominant Market Position: DIAL is the clear leader in Sri Lanka's mobile, home broadband, and pay-TV segments. Its 2024 merger with Airtel Lanka is expected to further consolidate its market share to over 60%.

Key Risk Factors to Monitor
Even for a low-risk stock, there are specific factors that may cause price fluctuations: 
Currency Exposure: Approximately 45% of DIAL's debt is in foreign currency. While significantly reduced from previous years, a sudden devaluation of the Sri Lankan Rupee can still impact profitability.
High Capital Expenditure: The company plans to invest USD 100 million over the next two years specifically for 5G expansion. Large infrastructure spending can limit free cash flow in the short term.
Macroeconomic Sensitivity: Slower growth in household purchasing power due to tax changes (like higher VAT) can lead to temporary declines in subscriber usage for non-essential services like Pay TV. 

Summary for Investors (March 2026)
Feature 	Assessment
Safety Level	High – "AAA" rated blue-chip stock.
Income Potential	Stable – Recommended dividend of Rs. 1.50 for 2026.
Growth Catalyst	5G Infrastructure – Leading the national 5G rollout.
Stock Stability	Defensive – Telecom services remain essential despite inflation.
Verdict: For risk-averse investors, DIAL serves as an excellent core holding. It provides a combination of capital safety (via its AAA rating) and reliable passive income through dividends, while its 5G leadership offers moderate long-term growth potential.


"""
},

# 15
{
"question": "Risks to consider before investing in Sri Lankan stocks",
"expected": """In 2026, investing in the Sri Lankan share market requires navigating a "selective phase" where broad-based recovery has ended and returns are driven by individual company fundamentals. While macroeconomic stability has strengthened, several specific risks have emerged in early 2026 that you must consider. 

1. Geopolitical & External Shocks
The most immediate risk in March 2026 is the escalating conflict in the Middle East, specifically following military strikes involving the U.S., Israel, and Iran. 

Energy Prices: Global Brent crude has surged past $90 per barrel, leading to domestic fuel price hikes and potential supply disruptions if the Strait of Hormuz remains closed.
Export Logistics: Rerouting vessels around the Cape of Good Hope to avoid combat zones has increased transit times for Sri Lankan apparel and rubber by 10–14 days, raising freight costs and hurting competitiveness.
Remittances: Over 1.5 million Sri Lankans work in the Gulf; a regional conflict could freeze hiring and reduce vital foreign exchange inflows. 

2. Macroeconomic & Interest Rate Risks
While inflation is currently low, undercurrents of concern are growing regarding medium-term stability. 
Rising Interest Rates: Yields on government securities are on an upward trend. The Average Weighted Prime Lending Rate (AWPR) is projected to rise to 10.0%–11.0% in the second half of 2026.
Inflation Supply Shocks: Destruction of supply chains and agriculture caused by Cyclone Ditwah in late 2025 is expected to cause a temporary rise in food inflation in early 2026.
Currency Depreciation: The Sri Lankan Rupee is expected to depreciate by approximately 5% during 2026, with year-end targets between Rs. 320.0–330.0 per USD. 

3. Fiscal & Policy Risks
Investors must account for a tightening tax and regulatory environment designed to meet IMF debt sustainability targets. 
Tax Burden: The 2026 Budget has reduced the VAT registration threshold from Rs. 60 million to Rs. 36 million, bringing thousands of smaller firms into the tax net.
Policy Inconsistency: Concerns remain that populist political decisions could derail fiscal consolidation as the government faces pressure to maintain public support.
Banking Sector Vulnerabilities: Despite recovery, banks face issues including non-performing loans (NPLs) exceeding 12% and a high overall tax burden of 57%. 

4. Market & Structural Risks
Liquidity Constraints: Trading in many stocks remains thin; the largest 100 firms often include examples where risk measures are less meaningful due to low trading volume.
Asset Repricing: Rapid interest rate adjustments in 2026 are causing sudden "rate re-pricing," which can lead to sharp equity corrections as investors shift capital back to fixed-income assets. 

Summary of Risk Profile (March 2026)
Risk Category 	Level	Impact on Investors
Geopolitical	High	Higher energy costs; trade/shipping delays.
Interest Rate	Moderate	Rising borrowing costs; downward pressure on stock PEs.
Currency	Low-Moderate	Expected 5% depreciation during the year.
Fiscal/Tax	High	Broadened VAT base impacting SME profitability.
For a safer entry, the Colombo Stock Exchange (CSE) and the SEC are currently promoting Unit Trusts (Mutual Funds) as a way for first-time investors to mitigate these risks through professional diversification.

 """
},

# 16
{
"question": "How does political instability affect the stock market?",
"expected": """In 2026, political stability is a primary driver of the Colombo Stock Exchange (CSE), as the market transitions from a post-crisis recovery to a long-term stability phase. Political instability traditionally triggers panic selling and reduces investor confidence, particularly among foreign institutional investors. 

Key Impacts of Political Instability
Market Volatility: Unanticipated political events, such as constitutional crises or sudden policy shifts, significantly increase price volatility. Historically, events like the 2018 constitutional crisis caused immediate, though sometimes mixed, reactions in the All Share Price Index (ASPI) as investors weighed the likelihood of economic resolution versus chaos.
Foreign Capital Outflows: Instability is a major deterrent for foreign investment. Periods of conflict or political unrest have historically caused the market to shrink and become unpopular with the international business community.
Policy Continuity Risk: Investors in 2026 are heavily focused on policy consistency. Any perceived threat to the ongoing IMF-supported reform program or fiscal discipline can lead to a "defensive crouch," where investors halt capital allocation due to systemic uncertainty.
Sector-Specific Hits: Political instability and unexpected government interventions primarily affect the risk-return structure of the banking and financial services sectors. 

Current Outlook (2026)
As of early 2026, the political landscape is rated as low risk due to the governing party's strong mandate and commitment to the IMF program. This stability has bolstered the 2026 economic outlook, allowing for: 

Moderate Growth: A transition toward a "selective phase" in the equity market where returns depend more on company fundamentals than broad-based sentiment.
Investor Confidence: A strong mandate has enabled the government to maintain consistent policies, which is a major "sentiment creator" for the CSE.
Rerating of Sectors: Stability has allowed for the rerating of certain sectors based on strong returns on equity (ROE) rather than political risk premiums. 

Conversely, any shift away from reform momentum is flagged by analysts as a "medium-term warning signal" that could destabilize the hard-won economic progress.

"""
},

# 17
{
"question": "Growth potential for SINGER Sri Lanka",
"expected": """In 2026, the growth potential for Singer (Sri Lanka) PLC (SINS) is viewed as constructive, driven by a robust recovery in consumer demand and significantly improved profitability. After successfully navigating the inventory crises of previous years, the company has transitioned into a "well-rounded investment profile" with a sustained uptrend in its share price. 

Key Growth Drivers (2026)
Consumer Demand Recovery: Fitch Ratings projects revenue growth of 10% for FY2026, following a strong 18% recovery in FY2025. This is supported by an expected average GDP growth of 3.5% in 2025–2026 and rising per capita income, which is projected to reach USD 4,270 by the end of 2026.
Strong Earnings Momentum: For the quarter ended December 2025, Group profits rose 47% to Rs. 2.1 billion, fueled primarily by the home appliances and financial services segments.
Improving Profit Margins: EBITDAR margins are forecast to stabilize at 10% in FY2026, up from 8% in FY2024, as the company benefits from higher sales volumes and lower borrowing costs.
Strategic Diversification: Singer is expanding beyond its core 3,000+ stock-keeping units (SKUs) into adjacent categories such as light vehicles and agricultural equipment, while leveraging AI-driven CRM tools for hyper-personalized marketing. 

Investment Metrics (March 2, 2026)
Metric 	Current Status / Forecast
Share Price (SINS.N)	Rs. 83.50 – 85.00 (Recent high of Rs. 101.0 in Jan 2026)
Analyst Target Price	Rs. 107.80 (Average consensus)
Price/Earnings (P/E)	13.79 – 17.55
Dividend Yield	1.42% – 1.66%
Credit Rating	'AA-(lka)' with a Stable Outlook (Fitch)
Risks to Growth
High Leverage: The Group maintains high debt levels (approx. Rs. 70 billion), primarily due to its finance subsidiary, Singer Finance (Lanka) PLC.
Market Competition: While Singer is the largest retailer with over 400 stores, it faces stiff competition from peers like Abans PLC, which is currently rated one notch higher at 'AA(lka)' due to lower leverage.
External Economic Factors: Future performance remains sensitive to changes in consumer spending power, interest rate fluctuations (projected at 8.0%–8.5% for T-bills), and potential import cost increases. 

Verdict: For 2026, Singer stands out as a fundamentally strong retail franchise with positive medium-term prospects, benefiting from its dominant market share and the general recovery of the Sri Lankan consumer durables sector."""
},

# 18
{
"question": "Is NDB Bank a strong dividend-paying stock?",
"expected": """In 2026, National Development Bank PLC (NDB) is considered a moderate but improving dividend-paying stock, characterized by a stable yield but historically inconsistent payment growth compared to other top-tier Sri Lankan banks. While its yield is currently higher than the bottom 25% of dividend payers in the market, it remains below the top-tier average. 

Key Dividend Metrics (March 2026)
Current Dividend Yield: Approximately 3.3%.
Dividend Yield Rank: NDB's yield (3.5%) is higher than Commercial Bank (2.9%) but lower than Hatton National Bank (4.7%) and Sampath Bank (6.6%).
Payout Ratio: Very conservative at 16%, meaning the bank retains a large portion of earnings to fund its aggressive growth strategy rather than distributing it all to shareholders.
Next Dividend Announcement: Following NDB's record-high Rs. 11.0 billion profit in FY 2025, analysts expect the next dividend declaration in mid-March 2026. 

Performance vs. Strategy
The bank's "strong" status as a dividend stock is currently debated by analysts: 
Positive Outlook: NDB reached all-time high earnings in 2025, with profits doubling on a normalized basis. This "resilient base" led analysts to revise dividend projections for 2026 upward to approximately Rs. 7.00 per share (a projected 5% yield).
Conservative Payout: Historically, NDB has used a mix of cash and scrip dividends (e.g., the March 2025 dividend was Rs. 5.00 in cash and Rs. 3.00 in scrip) to preserve capital for its expanding loan book, which grew by 26.7% in 2025. 

Comparative Dividend Yields (2026)
Bank Name 	Current Dividend Yield
Sampath Bank (SAMP)	6.6%
Hatton National Bank (HNB)	4.7%
National Development Bank (NDB)	3.3% - 3.5%
Commercial Bank (COMB)	2.9%

Verdict: NDB is a reliable payer with strong earnings backing its distributions, but if your primary goal is maximizing immediate passive income, it is currently outperformed by peers like Sampath Bank.
"""
},

# 19
{
"question": "What is Sampath Bank’s financial outlook?",
"expected": """The financial outlook for Sampath Bank PLC (SAMP) in 2026 is bullish, following its highest-ever historical performance in 2025. The bank achieved record profitability, with its total asset base surpassing the Rs. 2 trillion milestone. Analysts maintain a "Maintain Buy" recommendation, projecting continued earnings growth through 2026. 

Record Performance and 2026 Projections
In 2025, Sampath Bank reported its highest-ever profit after tax (PAT) of Rs. 30.2 billion, an 11% year-on-year increase. When adjusted for one-off gains from the previous year, the normalized growth rate reached an impressive 22%.

Key Financial Highlights (2025–2026)
Asset Growth: The Group's asset base grew 12% to exceed Rs. 2.0 trillion in 2025, primarily driven by a 27% expansion in the gross loan book to Rs. 1.2 trillion.
Dividend Payout: The Board recommended a final cash dividend of Rs. 10.30 per share for FY2025, which is an increase of Rs. 0.95 from the previous year. This dividend is scheduled for payment on April 23, 2026.
Target Price: Analysts have set a target price for 2026 at Rs. 175.00, representing significant upside from the current price of Rs. 160.75 (as of late February 2026).
Asset Quality: Credit quality improved notably, with Stage 3 loans (non-performing) dropping to 9.6% by end-2025 from 13.7% in 2024. 

Strategic Outlook for 2026
Sampath Bank is shifting its strategy from a post-crisis recovery to long-term growth: 
Wealth Management: In January 2026, the bank established a new wealth management company to diversify income streams, currently awaiting final regulatory approval.
Capital Strength: The bank comfortably maintains capital adequacy above regulatory minimums, with a Total Capital Ratio of 17.65% as of end-2025.
Digital and ESG Leadership: Continued investment in technology and ESG initiatives, such as Green Fixed Deposits, are expected to enhance brand value and operational efficiency throughout 2026. 

For detailed reports and the latest market updates, you can visit the Sampath Bank Investor Relations page or the Colombo Stock Exchange (CSE) company profile.
"""
},

# 20
{
"question": "Is Aitken Spence a stable long-term investment?",
"expected": """In 2026, Aitken Spence PLC (SPEN) is considered a stable and fundamentally strong long-term investment, supported by its diversified business model and resilient financial recovery following the post-crisis period. As of March 2, 2026, the stock is trading at approximately Rs. 158.50. 
Simply Wall St
Simply Wall St
 +2
Key Stability Indicators
Diverse Revenue Streams: The conglomerate operates across 17 industries in 12 countries, including tourism, maritime, freight logistics, and strategic investments.
Strong Financial Recovery: For the first half of FY 2025/26 (ending September 30, 2025), the group recorded a 42% increase in Profit Before Tax (PBT) to Rs. 1.6 billion. In the previous full financial year (FY25), EBITDA reached a record Rs. 25.4 billion.
High Credit Rating: In February 2026, Fitch Ratings assigned its hotel subsidiary, Aitken Spence Hotel Holdings, a National Long-Term Rating of 'AA+(lka)' with a Stable Outlook, reflecting the strength of its parent company, Aitken Spence PLC.
Deleveraging: The group has successfully lowered its debt-to-equity ratio from 0.45 to 0.38 over the past year, improving its balance sheet resilience against external shocks.

Long-Term Outlook
Tourism Sector Leadership: Tourism remains the highest contributor to PBT (approx. 55%), benefiting from a surge in Sri Lankan tourist arrivals and a strong presence in the Maldives.
Consistent Dividends: The company maintains a steady dividend stream, recently paying Rs. 4.00 per share for FY25 with a payout ratio of roughly 30%.
Strategic Expansion: Future growth is anchored in new ventures, such as the Port City BPO joint venture and renewable energy projects, aimed at an average annual sustainable profit growth of 10%. 

Risk Consideration: Despite its stability, the group faces moderate exposure to Maldivian currency regulations and sovereign risk, as a significant portion of its hotel EBITDA is generated there while debt remains primarily with Sri Lankan banks. 

For more information, you can review the latest Investor Relations reports on their website.

"""
}



]

# =====================================================
# SIMILARITY FUNCTION
# =====================================================

def calculate_similarity(text1, text2):
    vectorizer = TfidfVectorizer().fit_transform([text1, text2])
    vectors = vectorizer.toarray()
    similarity = cosine_similarity([vectors[0]], [vectors[1]])[0][0]
    return round(similarity * 100, 2)


# =====================================================
# RUN TESTS
# =====================================================

token = get_token()  # Get valid JWT token

HEADERS = {
    "Authorization": f"Bearer {token}"   # FIXED
}

total_score = 0
successful_tests = 0

print("\n================ MODEL ACCURACY TEST ================\n")

for i, test in enumerate(test_cases, start=1):

    response = requests.post(
        ASK_URL,
        headers=HEADERS,
        json={"question": test["question"]}
    )

    if response.status_code != 200:
        print(f"Error in Question {i}: {response.text}")
        continue

    model_answer = response.json().get("explanation", "")

    similarity_score = calculate_similarity(
        test["expected"],
        model_answer
    )

    total_score += similarity_score
    successful_tests += 1

    print(f"Question {i}: Similarity Score: {similarity_score}%")

# =====================================================
# FINAL ACCURACY
# =====================================================

if successful_tests == 0:
    print("\nNo successful test cases.")
else:
    average_accuracy = round(total_score / successful_tests, 2)

    print("\n=====================================================")
    print(f"FINAL MODEL ACCURACY: {average_accuracy}%")
    print("=====================================================")
