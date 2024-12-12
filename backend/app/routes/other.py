from flask import Blueprint, render_template

other_bp = Blueprint('privacy_policy', __name__)



@other_bp.route('/privacy-policy')
def privacy_policy():
    """
    Обработчик маршрута для страницы политики конфиденциальности.

    Возвращает HTML-шаблон для страницы с политикой конфиденциальности.

    Returns:
        str: Сгенерированный HTML-контент страницы 'privacy_policy.html'.
    """
    return render_template('privacy_policy.html')

@other_bp.route('/terms-of-service')
def terms_of_service():
    """
    Обработчик маршрута для страницы условий использования.

    Возвращает HTML-шаблон для страницы с условиями использования.

    Returns:
        str: Сгенерированный HTML-контент страницы 'terms_of_service.html'.
    """
    return render_template('terms_of_service.html')