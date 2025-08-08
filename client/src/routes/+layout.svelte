<script lang="ts">
import '../app.css';
import { browser } from '$app/environment';
import { afterNavigate } from '$app/navigation';
import { incrementNavigationCount } from '$lib/stores/navigation';
import { QueryClient, QueryClientProvider } from '@tanstack/svelte-query';

let { children } = $props();

const queryClient = new QueryClient({
	defaultOptions: {
		queries: {
			enabled: browser
		}
	}
});

afterNavigate(incrementNavigationCount);
</script>

<QueryClientProvider client={queryClient}>
	{@render children()}
</QueryClientProvider>
