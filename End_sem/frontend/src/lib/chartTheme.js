/**
 * Shared Recharts tooltip / cursor styling — dark glass, no white default box.
 */

export const chartTooltipContentStyle = {
  backgroundColor: 'rgba(9, 9, 14, 0.96)',
  border: '1px solid rgba(34, 211, 238, 0.28)',
  borderRadius: 10,
  boxShadow: '0 12px 40px rgba(0, 0, 0, 0.55)',
  padding: '10px 12px',
};

export const chartTooltipLabelStyle = {
  color: '#d4d4d8',
  fontSize: 12,
  fontWeight: 500,
  marginBottom: 4,
};

export const chartTooltipItemStyle = {
  color: '#fafafa',
  fontSize: 13,
};

export const chartTooltipProps = {
  contentStyle: chartTooltipContentStyle,
  labelStyle: chartTooltipLabelStyle,
  itemStyle: chartTooltipItemStyle,
  wrapperStyle: { outline: 'none', zIndex: 100 },
  cursor: { stroke: 'rgba(34, 211, 238, 0.35)', strokeWidth: 1 },
};

export const chartTooltipPropsNoCursor = {
  ...chartTooltipProps,
  cursor: false,
};
