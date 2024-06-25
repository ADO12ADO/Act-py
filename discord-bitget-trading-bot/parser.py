def parse_message(message):
    lines = message.split('\n')
    token = lines[0].split('$')[1]
    entry_price = float(lines[1].split(': ')[1])
    invalidation_level = float(lines[2].split(': ')[1])
    target_prices = list(map(float, lines[3].split(': ')[1].split('|')))

    return {
        'token': token,
        'entry_price': entry_price,
        'invalidation_level': invalidation_level,
        'target_prices': target_prices,
    }
