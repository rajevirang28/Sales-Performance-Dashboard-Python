import os
import pandas as pd
import matplotlib.pyplot as plt

# ----------------------------------

# SETTINGS

# ----------------------------------

plt.style.use('default')

os.makedirs("images", exist_ok=True)

# ----------------------------------

# LOAD DATA

# ----------------------------------

df = pd.read_csv("data/sales.csv", encoding="latin1")

df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

df["Order Date"] = pd.to_datetime(df["Order Date"])

# ----------------------------------

# KPI VALUES

# ----------------------------------

total_sales = df["Sales"].sum()
total_orders = len(df)
total_products = df["Product Name"].nunique()
total_regions = df["Region"].nunique()

# ----------------------------------

# AGGREGATIONS

# ----------------------------------

monthly_sales = (
df.groupby(df["Order Date"].dt.to_period("M"))["Sales"]
.sum()
)

monthly_sales.index = monthly_sales.index.astype(str)

region_sales = (
df.groupby("Region")["Sales"]
.sum()
.sort_values(ascending=False)
)

category_sales = (
df.groupby("Category")["Sales"]
.sum()
)

top_products = (
df.groupby("Product Name")["Sales"]
.sum()
.sort_values(ascending=False)
.head(10)
)

# ----------------------------------

# FIGURE

# ----------------------------------

fig = plt.figure(
figsize=(18, 10),
facecolor="white"
)

fig.suptitle(
"SALES PERFORMANCE DASHBOARD",
fontsize=28,
fontweight="bold",
color="#0A0F2C"
)

# ----------------------------------

# KPI CARDS

# ----------------------------------

card_style = dict(
boxstyle="round,pad=0.6",
facecolor="#F8FBFF",
edgecolor="#4A90E2",
linewidth=1.5
)

fig.text(
0.10,
0.90,
f"Total Sales\n${total_sales:,.0f}",
fontsize=15,
ha="center",
va="center",
bbox=card_style
)

fig.text(
0.35,
0.90,
f"Orders\n{total_orders:,}",
fontsize=15,
ha="center",
va="center",
bbox=card_style
)

fig.text(
0.60,
0.90,
f"Products\n{total_products:,}",
fontsize=15,
ha="center",
va="center",
bbox=card_style
)

fig.text(
0.85,
0.90,
f"Regions\n{total_regions}",
fontsize=15,
ha="center",
va="center",
bbox=card_style
)

# ----------------------------------

# GRID LAYOUT

# ----------------------------------

gs = fig.add_gridspec(
2,
12,
left=0.05,
right=0.98,
top=0.80,
bottom=0.06,
hspace=0.40,
wspace=0.60
)

# ----------------------------------

# MONTHLY TREND

# ----------------------------------

ax1 = fig.add_subplot(gs[0, 0:6])

monthly_sales.plot(
ax=ax1,
marker="o",
linewidth=2.5,
color="#1E88E5"
)

ax1.set_title(
"Monthly Sales Trend",
fontsize=16,
fontweight="bold"
)

ax1.set_xlabel("")
ax1.set_ylabel("Sales")
ax1.grid(True, alpha=0.3)

# ----------------------------------

# REGION SALES

# ----------------------------------

ax2 = fig.add_subplot(gs[0, 6:12])

region_sales.plot(
kind="bar",
ax=ax2,
color="#1E88E5"
)

ax2.set_title(
"Sales by Region",
fontsize=16,
fontweight="bold"
)

ax2.set_xlabel("")
ax2.set_ylabel("Revenue")
ax2.grid(axis="y", alpha=0.3)

# ----------------------------------

# DONUT CHART

# ----------------------------------

ax3 = fig.add_subplot(gs[1, 0:4])

colors = [
"#1E88E5",
"#FB8C00",
"#F4511E"
]

wedges, texts, autotexts = ax3.pie(
    category_sales,
    colors=colors,
    startangle=90,
    autopct="%1.1f%%",
    pctdistance=0.75,
    center=(-2, 0),
    wedgeprops=dict(
        width=0.45,
        edgecolor="white"
    )
)

ax3.legend(
    wedges,
    category_sales.index,
    loc="center right",
    bbox_to_anchor=(-0.15, 0.5),
    frameon=False
)

ax3.set_title(
"Sales by Category",
fontsize=16,
fontweight="bold"
)

# ----------------------------------

# TOP PRODUCTS

# ----------------------------------

ax4 = fig.add_subplot(gs[1, 5:12])

top_products.sort_values().plot(
kind="barh",
ax=ax4,
color="#1E88E5"
)

ax4.set_title(
"Top 10 Products",
fontsize=16,
fontweight="bold"
)

ax4.set_xlabel("Sales")
ax4.set_ylabel("")

ax4.tick_params(
axis="y",
labelsize=9
)

ax4.grid(
axis="x",
alpha=0.3
)

# ----------------------------------

# SAVE

# ----------------------------------

plt.savefig(
"images/sales_dashboard.png",
dpi=300,
bbox_inches="tight"
)

plt.show()

print("=" * 50)
print("SALES PERFORMANCE DASHBOARD GENERATED")
print("=" * 50)

print(f"Total Sales : ${total_sales:,.2f}")
print(f"Orders : {total_orders:,}")
print(f"Products : {total_products:,}")
print(f"Regions : {total_regions}")

print("Dashboard created successfully!")
print("Saved as images/sales_dashboard.png")