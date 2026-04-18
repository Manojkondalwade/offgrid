tailwind.config = {
  theme: {
    extend: {
      colors: {
        bg: {
          DEFAULT: '#0a0a0f',
          2: '#111118',
          3: '#18181f',
        },
        surface: {
          DEFAULT: '#1e1e28',
          2: '#252530',
        },
        border: {
          DEFAULT: '#2a2a38',
          2: '#333345',
        },
        accent: {
          DEFAULT: '#7c6af7',
          2: '#a89cf7',
          glow: 'rgba(124,106,247,0.18)',
        },
        green: {
          DEFAULT: '#3ecf8e',
          dim: 'rgba(62,207,142,0.12)',
        },
        orange: {
          DEFAULT: '#f59e0b',
          dim: 'rgba(245,158,11,0.12)',
        },
        red: {
          DEFAULT: '#ef4444',
          dim: 'rgba(239,68,68,0.1)',
        },
        text: {
          DEFAULT: '#e8e8f0',
          2: '#9999b3',
          3: '#5a5a78',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
        display: ['Inter', 'sans-serif'],
      },
      boxShadow: {
        glow: '0 0 40px rgba(124, 106, 247, 0.4)',
        soft: '0 4px 24px rgba(0, 0, 0, 0.4)',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
      }
    }
  }
}
