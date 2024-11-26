from flask import Blueprint, render_template, request
from .forms import WatchRecommendationForm
import pandas as pd

main = Blueprint('main', __name__)

# Load datasets
purchase_data = pd.read_excel('/Users/harryxu/FYP_App/data/Purchase records.xlsx', sheet_name='records (5)')
watch_data = pd.read_excel('/Users/harryxu/FYP_App/data/Watch Collections.xlsx', sheet_name='Sheet1')

purchase_data = purchase_data.dropna()
# watch_data = watch_data.dropna()

print("purchase_data:", purchase_data)

print("watch_data", watch_data)


@main.route('/', methods=['GET', 'POST'])
def home():
    form = WatchRecommendationForm()
    print("form:", form)
    if form.validate_on_submit():
        # Process form data
        lifestyle = form.lifestyle.data
        material = form.material.data
        price_range = form.price_range.data

        print("lifestyle:", lifestyle, "material:", material, "price_range:", price_range)
        # Filter data
        recommendations = watch_data[
            (watch_data['Style'].str.contains(lifestyle, case=False)) &
            (watch_data['Material'].str.contains(material, case=False)) &
            (watch_data['Price'].str.contains(price_range, case=False))
        ].head(5)

        if len(recommendations) == 0:
            recommendations = watch_data.sample(5)

        print(list(recommendations.columns))
        print("recommendations:", recommendations)
        return render_template('result.html', recommendations=recommendations)

    return render_template('form.html', form=form)
