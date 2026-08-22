from datetime import datetime


VALID_REPORT_TYPES = {"summary", "detailed", "forecast"}
VALID_OUTPUT_FORMATS = {"pdf", "excel", "html", "json"}


def validate_report_parameters(sales_data, report_type, date_range, output_format):
    """Validate inputs that control report generation."""
    if not sales_data or not isinstance(sales_data, list):
        raise ValueError("Sales data must be a non-empty list")
    if report_type not in VALID_REPORT_TYPES:
        raise ValueError("Report type must be 'summary', 'detailed', or 'forecast'")
    if output_format not in VALID_OUTPUT_FORMATS:
        raise ValueError("Output format must be 'pdf', 'excel', 'html', or 'json'")
    if date_range and ("start" not in date_range or "end" not in date_range):
        raise ValueError("Date range must include 'start' and 'end' dates")


def filter_sales_by_date_range(sales_data, date_range):
    """Return sales inside an optional inclusive date range."""
    if not date_range:
        return sales_data

    start_date = datetime.strptime(date_range["start"], "%Y-%m-%d")
    end_date = datetime.strptime(date_range["end"], "%Y-%m-%d")
    if start_date > end_date:
        raise ValueError("Start date cannot be after end date")

    return [
        sale
        for sale in sales_data
        if start_date <= datetime.strptime(sale["date"], "%Y-%m-%d") <= end_date
    ]


def apply_sales_filters(sales_data, filters):
    """Apply optional field-based filters."""
    if not filters:
        return sales_data

    filtered_data = sales_data
    for key, value in filters.items():
        if isinstance(value, list):
            filtered_data = [sale for sale in filtered_data if sale.get(key) in value]
        else:
            filtered_data = [sale for sale in filtered_data if sale.get(key) == value]
    return filtered_data


def calculate_sales_metrics(sales_data):
    """Calculate summary metrics for a non-empty sales list."""
    total_sales = sum(sale["amount"] for sale in sales_data)
    max_sale = max(sales_data, key=lambda sale: sale["amount"])
    min_sale = min(sales_data, key=lambda sale: sale["amount"])
    return {
        "total_sales": total_sales,
        "transaction_count": len(sales_data),
        "average_sale": total_sales / len(sales_data),
        "max_sale": {
            "amount": max_sale["amount"],
            "date": max_sale["date"],
            "details": max_sale,
        },
        "min_sale": {
            "amount": min_sale["amount"],
            "date": min_sale["date"],
            "details": min_sale,
        },
    }


def group_sales_data(sales_data, grouping, total_sales):
    """Create grouping statistics in the original report shape."""
    if not grouping:
        return None

    groups = {}
    for sale in sales_data:
        key = sale.get(grouping, "Unknown")
        groups.setdefault(key, {"count": 0, "total": 0})
        groups[key]["count"] += 1
        groups[key]["total"] += sale["amount"]

    output_groups = {}
    for key, data in groups.items():
        output_groups[key] = {
            "count": data["count"],
            "total": data["total"],
            "average": data["total"] / data["count"],
            "percentage": (data["total"] / total_sales) * 100,
        }
    return {"by": grouping, "groups": output_groups}


def build_detailed_transactions(sales_data):
    """Copy transactions and add the original calculated fields."""
    transactions = []
    for sale in sales_data:
        transaction = dict(sale)
        if "tax" in sale and "amount" in sale:
            transaction["pre_tax"] = sale["amount"] - sale["tax"]
        if "cost" in sale and "amount" in sale:
            transaction["profit"] = sale["amount"] - sale["cost"]
            transaction["margin"] = (transaction["profit"] / sale["amount"]) * 100
        transactions.append(transaction)
    return transactions


def calculate_sales_forecast(sales_data):
    """Calculate monthly totals, growth rates, and three projected months."""
    monthly_sales = {}
    for sale in sales_data:
        sale_date = datetime.strptime(sale["date"], "%Y-%m-%d")
        month_key = f"{sale_date.year}-{sale_date.month:02d}"
        monthly_sales[month_key] = monthly_sales.get(month_key, 0) + sale["amount"]

    sorted_months = sorted(monthly_sales)
    growth_rates = []
    for index in range(1, len(sorted_months)):
        previous_amount = monthly_sales[sorted_months[index - 1]]
        current_amount = monthly_sales[sorted_months[index]]
        if previous_amount > 0:
            growth_rates.append(((current_amount - previous_amount) / previous_amount) * 100)

    average_growth_rate = sum(growth_rates) / len(growth_rates) if growth_rates else 0
    projected_sales = {}
    if sorted_months:
        last_month = sorted_months[-1]
        last_amount = monthly_sales[last_month]
        year, month = map(int, last_month.split("-"))
        for _ in range(3):
            month += 1
            if month > 12:
                month = 1
                year += 1
            forecast_month = f"{year}-{month:02d}"
            last_amount = last_amount * (1 + average_growth_rate / 100)
            projected_sales[forecast_month] = last_amount

    return {
        "monthly_sales": monthly_sales,
        "growth_rates": {
            sorted_months[index]: growth_rates[index - 1]
            for index in range(1, len(sorted_months))
        },
        "average_growth_rate": average_growth_rate,
        "projected_sales": projected_sales,
    }


def generate_chart_data(sales_data, grouping):
    """Build sales-over-time and optional grouped chart data."""
    date_sales = {}
    for sale in sales_data:
        date_sales[sale["date"]] = date_sales.get(sale["date"], 0) + sale["amount"]

    dates = sorted(date_sales)
    charts = {
        "sales_over_time": {
            "labels": dates,
            "data": [date_sales[date] for date in dates],
        }
    }

    if grouping:
        grouped_totals = {}
        for sale in sales_data:
            key = sale.get(grouping, "Unknown")
            grouped_totals[key] = grouped_totals.get(key, 0) + sale["amount"]
        charts[f"sales_by_{grouping}"] = {
            "labels": list(grouped_totals.keys()),
            "data": list(grouped_totals.values()),
        }
    return charts


def handle_empty_report(report_type, output_format):
    print("Warning: No data matches the specified criteria")
    if output_format == "json":
        return {"message": "No data matches the specified criteria", "data": []}
    return _generate_empty_report(report_type, output_format)


def generate_report_output(report_data, output_format, include_charts):
    if output_format == "json":
        return report_data
    if output_format == "html":
        return _generate_html_report(report_data, include_charts)
    if output_format == "excel":
        return _generate_excel_report(report_data, include_charts)
    return _generate_pdf_report(report_data, include_charts)


def generate_sales_report(
    sales_data,
    report_type="summary",
    date_range=None,
    filters=None,
    grouping=None,
    include_charts=False,
    output_format="pdf",
):
    """Generate a sales report by coordinating focused helper functions."""
    validate_report_parameters(sales_data, report_type, date_range, output_format)
    sales_data = filter_sales_by_date_range(sales_data, date_range)
    sales_data = apply_sales_filters(sales_data, filters)

    if not sales_data:
        return handle_empty_report(report_type, output_format)

    metrics = calculate_sales_metrics(sales_data)
    report_data = {
        "report_type": report_type,
        "date_generated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "date_range": date_range,
        "filters": filters,
        "summary": metrics,
    }

    grouping_data = group_sales_data(sales_data, grouping, metrics["total_sales"])
    if grouping_data:
        report_data["grouping"] = grouping_data
    if report_type == "detailed":
        report_data["transactions"] = build_detailed_transactions(sales_data)
    if report_type == "forecast":
        report_data["forecast"] = calculate_sales_forecast(sales_data)
    if include_charts:
        report_data["charts"] = generate_chart_data(sales_data, grouping)

    return generate_report_output(report_data, output_format, include_charts)


# Output helper functions are intentionally left as starter stubs.
def _generate_empty_report(report_type, output_format):
    pass


def _generate_html_report(report_data, include_charts):
    pass


def _generate_excel_report(report_data, include_charts):
    pass


def _generate_pdf_report(report_data, include_charts):
    pass
