document.addEventListener("DOMContentLoaded", async () => {
    const quoteId = window.location.pathname.split("/").filter(Boolean).pop();
    const apiUrl = `/api/quotes/${quoteId}/`;
    const nameInput = document.querySelector("#name");
    const nfeInput = document.querySelector("#nfe");
    const observationsInput = document.querySelector("#observations");
    const discountInput = document.querySelector("#discount");
    const isQuoteInput = document.querySelector("#is_quote");
    const customerSelect = document.querySelector("[name='customer']");

    const selectedProducts = document.querySelector("#selectedProducts");
    const paymentsContainer = document.querySelector("#paymentMethodsContainer");

    let addedProducts = [];
    let paymentMethods = [];

    // Aguarda o select de cliente estar populado
    function waitForCustomerOption(customerId, maxRetries = 20) {
        return new Promise((resolve, reject) => {
            let attempts = 0;
            const interval = setInterval(() => {
                const option = customerSelect.querySelector(`option[value="${customerId}"]`);
                if (option) {
                    option.selected = true;
                    clearInterval(interval);
                    resolve();
                }
                attempts++;
                if (attempts >= maxRetries) {
                    clearInterval(interval);
                    reject(new Error("Cliente não carregado no select."));
                }
            }, 200);
        });
    }

    // Renderiza os produtos na tabela
    function renderSelectedProducts() {
        if (addedProducts.length === 0) {
            selectedProducts.innerHTML = `<tr><td colspan="5" class="text-center">Nenhum produto adicionado.</td></tr>`;
            return;
        }

        selectedProducts.innerHTML = addedProducts.map(product => `
            <tr>
                <td>${product.name}</td>
                <td>
                    <input type="number" class="form-control form-control-sm" value="${product.quantity}" min="1"
                        onchange="updateQuantity(${product.id}, this.value)" />
                </td>
                <td>
                    <input type="number" class="form-control form-control-sm" value="${Number(product.price).toFixed(2)}"
                        min="0" step="0.01"
                        onchange="updatePrice(${product.id}, this.value)" />
                </td>
                <td>R$ ${(product.price * product.quantity).toFixed(2)}</td>
                <td>
                    <button type="button" class="btn btn-sm btn-danger" onclick="removeProduct(${product.id})">Remover</button>
                </td>
            </tr>
        `).join("");

        const total = addedProducts.reduce((sum, p) => sum + Number(p.price) * p.quantity, 0);
        selectedProducts.innerHTML += `
            <tr>
                <td colspan="3" class="text-end"><strong>Total:</strong></td>
                <td colspan="2"><strong>R$ ${total.toFixed(2)}</strong></td>
            </tr>
        `;
    }

    // Renderiza os métodos de pagamento
    function renderPayments() {
        paymentsContainer.innerHTML = paymentMethods.map((payment, index) => {
            let extraFields = "";

            if (payment.payment_type === "CR") {
                extraFields += `
                    <div class="col">
                        <label>Parcelas</label>
                        <input type="number" class="form-control" min="1" value="${payment.credit_installments || 1}"
                            onchange="updatePayment(${index}, 'credit_installments', this.value)" />
                    </div>
                `;
            }

            if (payment.payment_type === "BO") {
                const boletos = payment.boletos || [];
                extraFields += `
                    <div class="col-12">
                        <label>Boletos</label>
                        <div id="boletoContainer${index}">
                            ${boletos.map((b, i) => `
                                <div class="row g-2 mb-1">
                                    <div class="col">
                                        <input type="number" class="form-control" placeholder="Valor" value="${b.value}"
                                            onchange="updateBoleto(${index}, ${i}, 'value', this.value)" />
                                    </div>
                                    <div class="col">
                                        <input type="date" class="form-control" value="${b.due_date}"
                                            onchange="updateBoleto(${index}, ${i}, 'due_date', this.value)" />
                                    </div>
                                    <div class="col-auto">
                                        <button class="btn btn-sm btn-danger" onclick="removeBoleto(${index}, ${i})">X</button>
                                    </div>
                                </div>
                            `).join("")}
                        </div>
                        <button type="button" class="btn btn-sm btn-secondary mt-2" onclick="addBoleto(${index})">Adicionar Boleto</button>
                    </div>
                `;
            }

            return `
                <div class="card mb-2 p-2">
                    <div class="row g-2 align-items-end">
                        <div class="col">
                            <label>Forma de Pagamento</label>
                            <select class="form-select" onchange="updatePayment(${index}, 'payment_type', this.value)">
                                <option value="DH" ${payment.payment_type === "DH" ? "selected" : ""}>Dinheiro</option>
                                <option value="PX" ${payment.payment_type === "PX" ? "selected" : ""}>PIX</option>
                                <option value="DB" ${payment.payment_type === "DB" ? "selected" : ""}>Débito</option>
                                <option value="CR" ${payment.payment_type === "CR" ? "selected" : ""}>Crédito</option>
                                <option value="BO" ${payment.payment_type === "BO" ? "selected" : ""}>Boleto</option>
                            </select>
                        </div>
                        ${payment.payment_type !== "BO" ? `
                        <div class="col">
                            <label>Valor</label>
                            <input type="number" class="form-control" value="${payment.amount || 0}"
                                onchange="updatePayment(${index}, 'amount', this.value)" />
                        </div>` : ""}
                        ${extraFields}
                        <div class="col-auto">
                            <button type="button" class="btn btn-danger" onclick="removePayment(${index})">
                                Remover
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }).join("");
    }

    // Atualiza métodos e boletos
    window.updatePayment = function (index, field, value) {
        if (field === "credit_installments") {
            paymentMethods[index][field] = parseInt(value);
        } else {
            paymentMethods[index][field] = value;
        }
        renderPayments();
    };

    window.removePayment = function (index) {
        paymentMethods.splice(index, 1);
        renderPayments();
    };

    window.addBoleto = function (paymentIndex) {
        if (!paymentMethods[paymentIndex].boletos) {
            paymentMethods[paymentIndex].boletos = [];
        }
        paymentMethods[paymentIndex].boletos.push({ value: "", due_date: "" });
        renderPayments();
    };

    window.addPaymentMethod = function () {
        paymentMethods.push({
            payment_type: "DH",
            amount: "",
            credit_installments: null,
            boletos: [],
        });
        renderPayments();
    };

    window.updateBoleto = function (paymentIndex, boletoIndex, field, value) {
        paymentMethods[paymentIndex].boletos[boletoIndex][field] = value;
        renderPayments();
    };

    window.removeBoleto = function (paymentIndex, boletoIndex) {
        paymentMethods[paymentIndex].boletos.splice(boletoIndex, 1);
        renderPayments();
    };

    // Produtos
    window.updatePrice = function (productId, newPrice) {
        const product = addedProducts.find(p => p.id === productId);
        if (product && newPrice >= 0) {
            product.price = parseFloat(newPrice);
            renderSelectedProducts();
        }
    };

    window.updateQuantity = function (productId, quantity) {
        const product = addedProducts.find(p => p.id === productId);
        if (product && quantity > 0) {
            product.quantity = parseInt(quantity, 10);
            renderSelectedProducts();
        }
    };

    window.removeProduct = function (productId) {
        addedProducts = addedProducts.filter(p => p.id !== productId);
        renderSelectedProducts();
    };

    // 🔥 Requisição de dados
    try {
        const response = await fetch(apiUrl);
        const { success, quote } = await response.json();

        if (!success || !quote) throw new Error("Dados inválidos.");

        // Preenche campos
        nameInput.value = quote.name || "";
        nfeInput.value = quote.nfe || "";
        observationsInput.value = quote.observations || "";
        discountInput.value = quote.discount || 0;
        isQuoteInput.checked = quote.is_quote || false;

        await waitForCustomerOption(quote.customer);

        // Produtos
        addedProducts = quote.products || [];
        renderSelectedProducts();

        // Pagamentos
        paymentMethods = quote.payments || [];
        renderPayments();
    } catch (err) {
        console.error("Erro ao carregar venda:", err);
        alert("Erro ao carregar os dados da venda.");
    }
});
