import locale
import os

# Simulate product data with English and Arabic names/descriptions
products = [
    {
        "id": "P001",
        "name_en": "Premium Coffee Maker",
        "name_ar": "صانعة قهوة فاخرة",
        "price_usd": 120.00,
        "description_en": "High-quality coffee maker for daily use.",
        "description_ar": "صانعة قهوة عالية الجودة للاستخدام اليومي.",
        "category": "Kitchen Appliances"
    },
    {
        "id": "P002",
        "name_en": "Smart Fitness Tracker",
        "name_ar": "جهاز تتبع اللياقة الذكي",
        "price_usd": 75.50,
        "description_en": "Monitor your health and activity.",
        "description_ar": "راقب صحتك ونشاطك.",
        "category": "Electronics"
    }
]

class ProductDisplayService:
    def __init__(self, region: str):
        self.region = region.upper()
        self._configure_region_settings()

    def _configure_region_settings(self):
        """
        Configures settings (currency, language, conversion rates) based on the region.
        This simulates how a platform like Trinavo would tailor its display and logic.
        """
        # Attempt to set a locale for number/currency formatting.
        # This can be system-dependent. For robust i18n, a library like 'babel' is preferred.
        try:
            locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
        except locale.Error:
            # Fallback for systems where 'en_US.UTF-8' is not available
            try:
                locale.setlocale(locale.LC_ALL, '') # Use system default
            except locale.Error:
                print("Warning: Could not set locale for currency formatting. Using basic string format.")
                # If locale fails entirely, we'll just format manually later.

        if self.region == "MENA":
            # For MENA, we simulate specific settings: Arabic language, Saudi Riyal, and a conversion rate.
            # This demonstrates a tailored approach for the MENA market.
            self.currency_symbol = "SAR" # Example: Saudi Riyal
            self.language = "ar"
            self.price_conversion_rate = 3.75 # Example: USD to SAR
        else: # Default to a Western market (e.g., US/EU)
            # For Western markets, default to English and USD.
            self.currency_symbol = "$"
            self.language = "en"
            self.price_conversion_rate = 1.0 # USD to USD

    def get_localized_price(self, price_usd: float) -> str:
        """
        Converts and formats the price according to the region's currency and locale.
        """
        converted_price = price_usd * self.price_conversion_rate
        try:
            # Use locale for currency formatting if available
            return f"{locale.currency(converted_price, symbol=False, grouping=True)} {self.currency_symbol}"
        except locale.Error:
            # Fallback if locale setting failed
            return f"{converted_price:.2f} {self.currency_symbol}"

    def get_localized_name(self, product: dict) -> str:
        """
        Returns the product name in the configured regional language.
        """
        if self.language == "ar":
            # Prioritize Arabic name for MENA region
            return product.get("name_ar", product["name_en"])
        return product["name_en"]

    def get_localized_description(self, product: dict) -> str:
        """
        Returns the product description in the configured regional language.
        """
        if self.language == "ar":
            # Prioritize Arabic description for MENA region
            return product.get("description_ar", product["description_en"])
        return product["description_en"]

    def apply_regional_offer(self, price_usd: float) -> float:
        """
        Applies region-specific business logic, like a promotional discount.
        This highlights how platforms can offer tailored experiences.
        """
        if self.region == "MENA":
            # Example: A special 10% discount for MENA customers,
            # reflecting a tailored marketing strategy for the region.
            return price_usd * 0.90
        return price_usd

    def display_product(self, product: dict):
        """
        Prints the localized and regionally-adjusted product information.
        """
        print(f"--- Product ID: {product['id']} ({self.region} context) ---")
        original_price = product['price_usd']
        price_after_offer = self.apply_regional_offer(original_price) # Apply regional offer

        print(f"Name: {self.get_localized_name(product)}")
        print(f"Description: {self.get_localized_description(product)}")
        print(f"Category: {product['category']}")
        print(f"Original Price (USD): {self.get_localized_price(original_price)}")
        # Display the price after applying the regional offer and converting to local currency
        print(f"Price (after regional offer): {self.get_localized_price(price_after_offer)}")
        print("-" * 30)


if __name__ == "__main__":
    print("Demonstrating tailored e-commerce experience by region:\n")

    # Scenario 1: Displaying products for a MENA region context
    print("--- Displaying products for MENA region (e.g., Saudi Arabia) ---")
    mena_service = ProductDisplayService("MENA")
    for product in products:
        mena_service.display_product(product)

    # Scenario 2: Displaying products for a Western region context (e.g., United States)
    print("\n--- Displaying products for Western (US) region ---")
    us_service = ProductDisplayService("US")
    for product in products:
        us_service.display_product(product)

    # Scenario 3: Displaying products for another Western region (e.g., Europe)
    # In this simplified example, EU defaults to the same settings as US for demonstration.
    print("\n--- Displaying products for Western (EU) region ---")
    eu_service = ProductDisplayService("EU")
    for product in products:
        eu_service.display_product(product)

    print("\nThis example illustrates how a platform can adapt language, currency, and business rules (like discounts) based on the target region, addressing the 'one-size-fits-all' problem.")
