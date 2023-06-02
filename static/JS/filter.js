const languageButtons = document.querySelectorAll('.language-btn');
const studiesContainer = document.querySelector('.cardlist__container')

languageButtons.forEach((button) => {
  button.addEventListener('click', async (e) => {
    const selectedLang = button.dataset.lang;

    try {
      const response = await fetch(`/studies/?lang=${selectedLang}`);
      console.log(response);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const html = await response.text();
      const parser = new DOMParser();
      const doc = parser.parseFromString(html, 'text/html');
      const studies = doc.querySelector('.cardlist__container');
      studiesContainer.innerHTML = studies.innerHTML;
    } catch (error) {
      console.log(error);
    }
  });
});
