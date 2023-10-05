function addForm(formContainerId, formsetName) {
    // 폼셋의 폼 개수 가져오기
    const formContainer = document.getElementById(formContainerId);
    const totalFormsInput = document.getElementById('id_' + formsetName + '-TOTAL_FORMS');
    const totalForms = parseInt(totalFormsInput.value);
    console.log(totalFormsInput);
    // 새로운 폼을 생성하고 필요한 수정을 수행
    const newForm = document.createElement('div');
    newForm.innerHTML = formContainer.innerHTML; // 첫 번째 폼 복제
    const inputs = newForm.querySelectorAll('input, select, textarea');
    console.log(newForm);

    for (let i = 0; i < inputs.length; i++) {
        const name = inputs[i].name.replace('-' + (totalForms - 1) + '-', '-' + totalForms + '-');
        const id = 'id_' + name;
        inputs[i].name = name;
        inputs[i].id = id;
        inputs[i].value = '';
        inputs[i].checked = false;
        inputs[i].classList.add('cyberpunk');  // class 속성을 추가할 때는 classList를 사용합니다.
    }

    // 새로운 폼을 폼셋에 추가
    formContainer.appendChild(newForm);

    // TOTAL_FORMS 업데이트
    totalFormsInput.value = totalForms + 1;
}


var productAddBtn = document.getElementById('add-product-form-btn');
productAddBtn.addEventListener('click', function(event){
    console.log("버튼")
    addForm('product-form-container', 'price');
})
var imageAddBtn = document.getElementById('add-image-form-btn');
imageAddBtn.addEventListener('click', function(event){
    console.log("버튼")
    addForm('image-form-container', 'image');
})