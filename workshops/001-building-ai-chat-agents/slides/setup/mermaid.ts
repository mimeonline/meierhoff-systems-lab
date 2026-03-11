import { defineMermaidSetup } from '@slidev/types'

export default defineMermaidSetup(() => {
  return {
    theme: 'base',
    themeVariables: {
      primaryColor: '#162132',
      primaryTextColor: '#f1f5f9',
      primaryBorderColor: '#388bd2',
      secondaryColor: '#0f172a',
      secondaryTextColor: '#f1f5f9',
      secondaryBorderColor: '#1e3a5f',
      tertiaryColor: '#0b1120',
      tertiaryTextColor: '#f1f5f9',
      tertiaryBorderColor: '#1e3a5f',
      lineColor: '#388bd2',
      textColor: '#f1f5f9',
      nodeBorder: '#388bd2',
      mainBkg: '#162132',
      nodeBkg: '#162132',
      clusterBkg: '#0f172a',
      clusterBorder: '#1e3a5f',
      edgeLabelBackground: '#0f172a',
      fontFamily: 'Inter, sans-serif',
      fontSize: '14px',
      noteBkgColor: '#162132',
      noteTextColor: '#f1f5f9',
      noteBorderColor: '#1e3a5f',
    },
  }
})
