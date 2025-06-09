document.addEventListener("DOMContentLoaded", function () {
    const customerApiUrl = "/api/customers/"; // URL da API de clientes
    const customerSelect = document.querySelector("[name='customer']");

    async function fetchCustomers() {
        try {
            const response = await fetch(customerApiUrl);
            const data = await response.json();
            const customers = data.customers || [];
            renderCustomerOptions(customers);
        } catch (error) {
            console.error("Erro ao buscar clientes:", error);
        }
    }

    function renderCustomerOptions(customers) {
        customerSelect.innerHTML = `
            <option hidden selected disabled>Selecione</option>
        `; // Reseta as opções existentes

        customers.forEach((customer) => {
            const option = document.createElement("option");
            option.value = customer.id;
            option.textContent = `${customer.name} (${customer.cpf_or_cnpj})`;
            
            if (customer.has_overdue_boleto) {
                option.classList.add("overdue");
            }

            customerSelect.appendChild(option);
        });
    }

    fetchCustomers();
});