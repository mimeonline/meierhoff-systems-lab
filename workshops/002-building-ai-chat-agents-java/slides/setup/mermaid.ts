import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => ({
  theme: 'base',
  themeVariables: {
    darkMode: true,
    background: '#0b1120',
    primaryColor: '#0f172a',
    primaryTextColor: '#f1f5f9',
    primaryBorderColor: '#388bd2',
    lineColor: '#7cc4f5',
    secondaryColor: '#0b1120',
    tertiaryColor: '#152035',
    clusterBkg: 'rgba(15, 23, 42, 0.7)',
    clusterBorder: '#1e3a5f',
    titleColor: '#94a3b8',
    edgeLabelBackground: '#0b1120',
    nodeTextColor: '#f1f5f9',
    fontFamily: 'Inter, sans-serif',
    fontSize: '13px',
  }
}))
