export function conditionChange() {
  const selectElement = document.getElementById('condition-select');
  const selectedOption = selectElement.querySelector('option[selected]');
  
  if (selectedOption) {
    selectElement.prepend(selectedOption);
  }

  function updateAction(event) {
    // 이벤트 객체에서 select 요소 가져오기
    const selectElement = event.target; 
    const selectedOption = selectElement.options[selectElement.selectedIndex].text;
    const message = `스터디 조건을 "${selectedOption}"으로 변경하겠습니까?`;
    alert(message);

    const form = document.getElementById('condition-form');
    const actionUrl = form.action.replace('/condition/0/', '/condition/' + selectElement.value + '/');
    form.action = actionUrl;
    form.submit();
  }

  // onchange 이벤트 핸들러 설정
  selectElement.onchange = updateAction;
}
