<script>
	import { onMount } from 'svelte';
	import { createClient } from '@supabase/supabase-js';

	import { setLocale } from '$lib/paraglide/runtime';
	import { page } from '$app/state';
	import { goto } from '$app/navigation';
	import { m } from '$lib/paraglide/messages.js';
	// Configuração do Supabase

	const supabaseUrl = 'https://dipsnjjphasmanpgglkz.supabase.co';
	const supabaseKey =
		'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRpcHNuampwaGFzbWFucGdnbGt6Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDM4MTEyOTgsImV4cCI6MjA1OTM4NzI5OH0.N3uGr9PJWMxOCNv5d0rfj3QwJ-BjWFat2G7dYFPvQ0U';

	const supabase = createClient(supabaseUrl, supabaseKey);

	let orgs = []; // Lista de todas as organizações disponíveis
	let selectedOrgId; // ID da organização selecionada pelo usuário
	let orgData = null; // Dados detalhados da organização selecionada

	// Busca todas as organizações ao montar o componente
	onMount(async () => {
		const { data, error } = await supabase.from('Org').select('*');

		if (!error) {
			orgs = data;
		}
	});

	// Quando o usuário seleciona uma organização, esta função carrega os dados relacionados
	async function fetchOrgWithDetails(orgId) {
		selectedOrgId = orgId;

		// Passo 1: Buscar dados da organização
		const { data: org } = await supabase.from('Org').select('*').eq('id', orgId).single();

		// Passo 2: Buscar produtos da organização
		const { data: products } = await supabase.from('Product').select('*').eq('org_id', orgId);

		// Passo 3: Buscar repositórios e configs por produto
		for (let product of products) {
			const { data: repositories } = await supabase
				.from('Repository')
				.select('*')
				.eq('product_id', product.id);

			for (let repo of repositories) {
				let { data: configs } = await supabase
					.from('RepositoryConfig')
					.select('*')
					.eq('repository_id', repo.id);

				if (!configs.length) {
					const { data: defaultConfigs } = await supabase.from('DefaultConfig').select('*');
					configs = defaultConfigs;
				}

				repo.configs = configs;
			}

			product.repositories = repositories;
		}

		org.products = products;
		orgData = org;
	}
</script>

<h1>{m.hello_world({ name: 'SvelteKit User' })}</h1>
<div>
	<button onclick={() => setLocale('en')}>en</button>
	<button onclick={() => setLocale('es')}>es</button>
	<button onclick={() => setLocale('pt')}>pt</button>
</div>
<h1>{m.hello_world({ name: 'Orgs' })}</h1>

<!-- Lista de organizações com botão para carregar detalhes -->
<ul>
	{#each orgs as org}
		<li>
			{org.nome}
			<button onclick={() => fetchOrgWithDetails(org.id)}>Ver detalhes</button>
		</li>
	{/each}
</ul>

<!-- Exibe os dados detalhados da organização selecionada -->
{#if orgData}
	<hr />
	<h2>Organização: {orgData.nome}</h2>
	<ul>
		{#each orgData.products as product}
			<li>
				Produto: {product.nome}
				<ul>
					{#each product.repositories as repo}
						<li>
							Repositório: {repo.nome}
							<ul>
								{#each repo.configs as cfg}
									<li>{cfg.chave}: {cfg.valor}</li>
								{/each}
							</ul>
						</li>
					{/each}
				</ul>
			</li>
		{/each}
	</ul>
{/if}
