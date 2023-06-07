const attendanceChart = document.getElementById('attendanceRate-chart');
const userPercentages = JSON.parse(
  document.getElementById('user_percentages').textContent
);
let delayed;

new Chart(attendanceChart, {
  type: 'bar',

  data: {
    labels: userPercentages.map((item) => item[0]),
    datasets: [
      {
        label: '출석률',
        data: userPercentages.map((item) => item[1]),
        backgroundColor: userPercentages.map((item,idx) => {
          if (idx === 0) return '#6C8E2D'
          if (idx === 1) return '#94B359'
          if (idx === 2) return '#BBD885'
        })
      },
    ],
  },
  options: {
    // scales: {
    //   y: {
    //     display: false, 
    //   },
    // },
    animation: {
      onComplete: () => {
        delayed = true;
      },
      delay: (context) => {
        let delay = 0;
        if (context.type === 'data' && context.mode === 'default' && !delayed) {
          delay = context.dataIndex * 300 + context.datasetIndex * 100;
        }
        return delay;
      },
    },
    maintainAspectRatio: false,
    
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += context.parsed.y + '%';
            return label;
          }
        }
      },
      legend: {
        display: false,
      },
    },
  },
});

const reviewChart = document.getElementById('reviewsRate-chart');
const userReviews = JSON.parse(
  document.getElementById('user_percentages').textContent
);
let reviewdelayed;

new Chart(reviewChart, {
  type: 'bar',

  data: {
    labels: userPercentages.map((item) => item[0]),
    datasets: [
      {
        label: '리뷰',
        data: userPercentages.map((item) => item[1]),
        backgroundColor: userPercentages.map((item,idx) => {
          if (idx === 0) return '#6C8E2D'
          if (idx === 1) return '#94B359'
          if (idx === 2) return '#BBD885'
        })
      },
    ],
  },
  options: {
    animation: {
      onComplete: () => {
        delayed = true;
      },
      delay: (context) => {
        let delay = 0;
        if (
          context.type === 'data' &&
          context.mode === 'default' &&
          !reviewdelayed
        ) {
          delay = context.dataIndex * 300 + context.datasetIndex * 100;
        }
        return delay;
      },
    },
    maintainAspectRatio: false,
    plugins: {
      tooltip: {
        callbacks: {
          label: (context) => {
            let label = context.dataset.label || '';
            if (label) {
              label += ': ';
            }
            label += context.parsed.y + '%';
            return label;
          }
        }
      },
      legend: {
        display: false,
      },
    },
  },
});
