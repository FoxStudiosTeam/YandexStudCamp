def postprocess_results(results):
    # Постобработка результатов от модели (можно добавить фильтрацию по confidence)
    return results.pred[0]  # Пример обращения к предсказаниям