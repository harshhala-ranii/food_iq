export enum HealthIssue {
  NONE = 'none',
  DIABETES = 'diabetes',
  OBESITY = 'obesity',
  CHOLESTEROL = 'cholesterol',
  HIGH_BP = 'high-bp',
  GLUTEN_INTOLERANCE = 'gluten intolerance',
  ACIDITY = 'acidity'
}

export const HealthIssueLabels: Record<HealthIssue, string> = {
  [HealthIssue.NONE]: 'None',
  [HealthIssue.DIABETES]: 'Diabetes',
  [HealthIssue.OBESITY]: 'Obesity',
  [HealthIssue.CHOLESTEROL]: 'Cholesterol',
  [HealthIssue.HIGH_BP]: 'High Blood Pressure',
  [HealthIssue.GLUTEN_INTOLERANCE]: 'Gluten Intolerance',
  [HealthIssue.ACIDITY]: 'Acidity'
}; 