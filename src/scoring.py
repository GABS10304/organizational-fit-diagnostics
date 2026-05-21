import pandas as pd

# Dimension definitions
DIMENSIONS = {
    'strategy': [
        'market_dynamics',
        'transformation_pressure',
        'strategy_adjustment',
        'customer_responsiveness',
        'industry_competitiveness',
        'innovation_importance',
        'regulatory_anticipation',
        'digital_maturity'
    ],
    'team': [
        'team_autonomy',
        'role_clarity',
        'priority_change_frequency',
        'skills_development',
        'data_usage',
        'efficiency_vs_innovation'
    ],
    'culture': [
        'cross_department_collaboration',
        'mistake_handling',
        'decision_transparency',
        'learning_promotion',
        'technology_adaptability',
        'collaboration_culture'
    ],
}

SCORE_THRESHOLDS = {
    'high': 7,
    'medium': 4,
}

RECOMMENDATIONS = {
    'strategy': {
        'low': 'Clarify strategic priorities. Run a strategy alignment workshop with leadership.',
        'medium': 'Strategy is partially aligned. Focus on improving feedback loops and roadmap transparency.',
        'high': 'Strong strategy foundation. Focus on sustaining momentum and market anticipation.'
    },
    'team': {
        'low': 'Teams lack autonomy or clarity. Introduce decision rights and clear role boundaries.',
        'medium': 'Team dynamics are developing. Invest in cross-functional collaboration and skills growth.',
        'high': 'Teams are effective and self-directed. Focus on scaling these practices.'
    },
    'culture': {
        'low': 'Culture shows signs of fear or silos. Prioritize psychological safety and transparency.',
        'medium': 'Culture is evolving. Reinforce learning behavior and reduce punitive reactions to failure.',
        'high': 'Culture supports learning and collaboration. Protect and deepen these behaviors.'
    }
}


def classify(score):
    if score >= SCORE_THRESHOLDS['high']:
        return 'high'
    elif score >= SCORE_THRESHOLDS['medium']:
        return 'medium'
    return 'low'


def score_row(row):
    scores = {}
    for dim, cols in DIMENSIONS.items():
        vals = [row[c] for c in cols if c in row and pd.notna(row[c])]
        avg = round(sum(vals) / len(vals), 2) if vals else None
        scores[f'{dim}_score'] = avg
        scores[f'{dim}_level'] = classify(avg) if avg else None
        scores[f'{dim}_recommendation'] = RECOMMENDATIONS[dim][classify(avg)] if avg else None

    dim_scores = {k: scores[f'{k}_score'] for k in DIMENSIONS if scores[f'{k}_score'] is not None}
    scores['largest_gap_area'] = min(dim_scores, key=dim_scores.get).capitalize() if dim_scores else None
    return scores


def run(input_csv, output_csv):
    df = pd.read_csv(input_csv)
    results = df.apply(score_row, axis=1, result_type='expand')
    output = pd.concat([df[['organization_type']], results], axis=1)
    output.to_csv(output_csv, index=False)
    print(f'Saved: {output_csv}')
    return output


if __name__ == '__main__':
    run('data/example_assessment.csv', 'examples/example_output.csv')
