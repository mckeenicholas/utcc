<script lang="ts">
import { browser } from "$app/environment";
import { goto } from "$app/navigation";
import { navigationCount, decrementNavigationCount } from "$lib/stores/navigation";

const getParentRoute = (path = window.location.pathname) => {
	if (path.endsWith("/")) {
		path = path.slice(0, -1);
	}

	return path.slice(0, path.lastIndexOf("/")) || "/";
};

const goBack = () => {
	if (!browser) {
		return;
	}

	const currentNavigationCount = $navigationCount;

	if (currentNavigationCount > 1) {
		decrementNavigationCount(2);
		window.history.back();
	} else {
		const parentRoute = getParentRoute();
		decrementNavigationCount();
		goto(parentRoute);
	}
};
</script>

<div class="ms-2 mt-2">
	<button
		onclick={goBack}
		class="inline-flex items-center rounded-md bg-gray-600 py-2 ps-3 pe-4 text-sm font-medium text-white transition-colors duration-150 hover:bg-gray-700"
	>
		<svg class="mr-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
			<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
		</svg>
		Back
	</button>
</div>
