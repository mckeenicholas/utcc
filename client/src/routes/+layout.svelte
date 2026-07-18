<script lang="ts">
import "../app.css";
import { afterNavigate } from "$app/navigation";
import { incrementNavigationCount } from "$lib/stores/navigation";

const { children } = $props();

afterNavigate(incrementNavigationCount);
</script>

{@render children()}
