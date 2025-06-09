// Variáveis globais
let products = [];
let addedProducts = [];
let paymentMethods = [];

// Inicializa ao carregar DOM
document.addEventListener("DOMContentLoaded", () => {
    // const quoteId = document.body.dataset.quoteId;
    const quoteId = window.quoteId;
    fetchQuote(quoteId);
    bindListeners();
});

// Carrega a venda existente
async function fetchQuote(quoteId) {
    try {
        const res = await fetch(`/api/quotes/${quoteId}/`);
        const data = await res.json();

        if (!data.success) throw new Error("API retornou erro");

        const quote = data.quote;

        // Preenche campos principais
        document.getElementById("name").value = quote.name;
        document.getElementById("nfe").value = quote.nfe;
        document.getElementById("observations").value = quote.observations;
        document.getElementById("discount").value = quote.discount || 0;
        document.getElementById("is_quote").checked = quote.is_quote;

        // Seleciona cliente
        const customerSelect = document.querySelector("select[name='customer']");
        customerSelect.value = quote.customer;

        // Preenche produtos e pagamentos
        addedProducts = quote.products.map(p => ({
            id: p.id,
            name: p.name,
            quantity: p.quantity,
            price: p.price
        }));

        paymentMethods = quote.payments.map(p => ({
            payment_type: p.payment_type,
            amount: p.amount,
            credit_installments: p.credit_installments,
            boletos: p.boletos
        }));

        renderSelectedProducts();
        renderPayments();
    } catch (err) {
        console.error(err);
        alert("Erro ao carregar os dados da venda.");
    }
}

// BIND EVENTOS
function bindListeners() {
    // Botão de adicionar produto
    document.getElementById("productSearch").addEventListener("input", async function () {
        const query = this.value.trim();
        if (!query) return;
        const response = await fetch(`/api/products/search/?search=${query}`);
        const data = await response.json();
        products = data.products || [];
        renderProductResults();
    });

    // Botão de adicionar forma de pagamento
    document.getElementById("addPaymentMethodBtn").addEventListener("click", () => {
        paymentMethods.push({ payment_type: "DH", amount: 0, credit_installments: null, boletos: [] });
        renderPayments();
    });

    // Submit do formulário
    document.getElementById("quoteForm").addEventListener("submit", handleSubmit);
}

// RENDERIZAÇÃO
function renderProductResults() {
    const container = document.getElementById("productResults");
    container.innerHTML = products.map(p => `
        <li class="list-group-item d-flex justify-content-between align-items-center">
            ${p.name} - ${p.category} - ${p.manufacturer} | ${p.weight}${p.unit_type}, ${p.size}, ${p.quantity_per_package} folhas
            <button type="button" class="btn btn-sm btn-success" onclick="addProduct(${p.id})">Adicionar</button>
        </li>
    `).join("");
}


function renderSelectedProducts() {
    const container = document.getElementById("selectedProducts");
    if (addedProducts.length === 0) {
        container.innerHTML = "<tr><td colspan='5' class='text-center'>Nenhum produto adicionado.</td></tr>";
        return;
    }

    let rows = addedProducts.map(p => `
        <tr>
            <td>${p.name}</td>
            <td><input type="number" min="1" class="form-control form-control-sm" value="${p.quantity}"
                onchange="updateProductQuantity(${p.id}, this.value)" /></td>
            <td><input type="number" step="0.01" class="form-control form-control-sm" value="${p.price}"
                onchange="updateProductPrice(${p.id}, this.value)" /></td>
            <td>R$ ${(p.quantity * p.price).toFixed(2)}</td>
            <td><button class="btn btn-danger btn-sm" onclick="removeProduct(${p.id})">Remover</button></td>
        </tr>
    `).join("");

    const total = addedProducts.reduce((acc, p) => acc + (p.price * p.quantity), 0);

    rows += `
        <tr>
            <td colspan="3" class="text-end"><strong>Total</strong></td>
            <td colspan="2"><strong>R$ ${total.toFixed(2)}</strong></td>
        </tr>
    `;

    container.innerHTML = rows;
}

function renderPayments() {
    const container = document.getElementById("paymentsContainer");
    container.innerHTML = paymentMethods.map((p, index) => {
        const isBoleto = p.payment_type === "BO";
        const isCredito = p.payment_type === "CR";

        let extra = "";

        if (isCredito) {
            extra = `
                <div class="col">
                    <label>Parcelas</label>
                    <input type="number" class="form-control" min="1" value="${p.credit_installments || 1}"
                        onchange="updatePayment(${index}, 'credit_installments', this.value)" />
                </div>
            `;
        }

        if (isBoleto) {
            extra = `
                <div class="col-12">
                    <label>Boletos</label>
                    ${renderBoletos(index)}
                    <button class="btn btn-sm btn-secondary mt-2" onclick="addBoleto(${index})">+ Boleto</button>
                </div>
            `;
        }

        return `
            <div class="card p-2 mb-2">
                <div class="row g-2 align-items-end">
                    <div class="col">
                        <label>Tipo</label>
                        <select class="form-select" onchange="updatePayment(${index}, 'payment_type', this.value)">
                            <option value="DH" ${p.payment_type === "DH" ? "selected" : ""}>Dinheiro</option>
                            <option value="PX" ${p.payment_type === "PX" ? "selected" : ""}>PIX</option>
                            <option value="DB" ${p.payment_type === "DB" ? "selected" : ""}>Débito</option>
                            <option value="CR" ${p.payment_type === "CR" ? "selected" : ""}>Crédito</option>
                            <option value="BO" ${p.payment_type === "BO" ? "selected" : ""}>Boleto</option>
                        </select>
                    </div>
                    ${!isBoleto ? `
                    <div class="col">
                        <label>Valor</label>
                        <input type="number" class="form-control" value="${p.amount}"
                            onchange="updatePayment(${index}, 'amount', this.value)" />
                    </div>
                    ` : ""}
                    ${extra}
                    <div class="col-auto">
                        <button class="btn btn-sm btn-danger" onclick="removePayment(${index})">Remover</button>
                    </div>
                </div>
            </div>
        `;
    }).join("");
}

function renderBoletos(paymentIndex) {
    const p = paymentMethods[paymentIndex];
    if (!p.boletos) p.boletos = [];

    return p.boletos.map((b, i) => `
        <div class="row mb-2 g-2">
            <div class="col">
                <input type="number" placeholder="Valor" class="form-control" value="${b.value}"
                    onchange="updateBoleto(${paymentIndex}, ${i}, 'value', this.value)" />
            </div>
            <div class="col">
                <input type="date" class="form-control" value="${b.due_date}"
                    onchange="updateBoleto(${paymentIndex}, ${i}, 'due_date', this.value)" />
            </div>
            <div class="col-auto">
                <button class="btn btn-sm btn-outline-danger" onclick="removeBoleto(${paymentIndex}, ${i})">X</button>
            </div>
        </div>
    `).join("");
}

// CONTROLES DE PRODUTO
function addProduct(productId) {
    const product = products.find(p => p.id === productId);
    if (!product || addedProducts.find(p => p.id === productId)) return;
    addedProducts.push({ ...product, quantity: 1, price: 0 });
    renderSelectedProducts();
}

function updateProductQuantity(id, qty) {
    const p = addedProducts.find(p => p.id === id);
    if (p) p.quantity = parseInt(qty, 10);
    renderSelectedProducts();
}

function updateProductPrice(id, price) {
    const p = addedProducts.find(p => p.id === id);
    if (p) p.price = parseFloat(price);
    renderSelectedProducts();
}

function removeProduct(id) {
    addedProducts = addedProducts.filter(p => p.id !== id);
    renderSelectedProducts();
}

// CONTROLES DE PAGAMENTO
function updatePayment(index, field, value) {
    paymentMethods[index][field] = field === "credit_installments" ? parseInt(value) : value;
    renderPayments();
}

function removePayment(index) {
    paymentMethods.splice(index, 1);
    renderPayments();
}

function addBoleto(index) {
    if (!paymentMethods[index].boletos) paymentMethods[index].boletos = [];
    paymentMethods[index].boletos.push({ value: "", due_date: "" });
    renderPayments();
}

function updateBoleto(paymentIndex, boletoIndex, field, value) {
    paymentMethods[paymentIndex].boletos[boletoIndex][field] = value;
}

function removeBoleto(paymentIndex, boletoIndex) {
    paymentMethods[paymentIndex].boletos.splice(boletoIndex, 1);
    renderPayments();
}

// ENVIO
async function handleSubmit(e) {
    e.preventDefault();

    const payload = {
        name: document.getElementById("name").value.trim(),
        nfe: document.getElementById("nfe").value.trim(),
        customer: document.querySelector("[name='customer']").value,
        observations: document.getElementById("observations").value.trim(),
        discount: parseInt(document.getElementById("discount").value || "0"),
        is_quote: document.getElementById("is_quote").checked,
        products: addedProducts.map(p => ({ id: p.id, quantity: p.quantity, price: p.price })),
        payments: paymentMethods.map(pm => ({
            payment_type: pm.payment_type,
            amount: pm.payment_type === "BO" ? null : Number(pm.amount),
            credit_installments: pm.payment_type === "CR" ? pm.credit_installments : null,
            boletos: pm.payment_type === "BO" ? pm.boletos : []
        }))
    };

    try {
        const csrfToken = document.cookie.match(/csrftoken=([^;]+)/)?.[1];
        const response = await fetch(window.location.pathname, {
            method: "POST",
            headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken },
            body: JSON.stringify(payload)
        });

        const result = await response.json();
        if (result.success) {
            alert("Orçamento atualizado com sucesso!");
            window.location.href = "/";
        } else {
            alert("Erro ao atualizar orçamento: " + result.error);
        }
    } catch (error) {
        console.error("Erro ao enviar orçamento:", error);
        alert("Erro ao enviar orçamento.");
    }
}
