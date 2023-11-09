---
title: Table test
---

<table class="sortable">
  {% for row in site.data.adventures %}
    {% if forloop.first %}
    <thead><tr>
      {% for pair in row %}
        <th>{{ pair[0] }}</th>
      {% endfor %}
    </tr></thead>
    {% endif %}

    {% if row.runtime == 2 %}
      {% tablerow pair in row %}
        {{ pair[1] }}
      {% endtablerow %}
    {% endif %}
{% endfor %}
</table>
    
<link href="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.css" rel="stylesheet" />
<script src="https://cdn.jsdelivr.net/gh/tofsjonas/sortable@latest/sortable.min.js"></script>