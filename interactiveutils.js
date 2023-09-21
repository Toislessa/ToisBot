import { isNotDefined, isDefined } from "react-stockcharts/lib/utils";

export function saveInteractiveNode(chartId) {
	return node => {
		this[`node_${chartId}`] = node;
	};
}

export function handleSelection(type, chartId) {
  console.log("handleSelection called", type, chartId);  // Adicione esta linha

  return selectionArray => {
      console.log("selectionArray:", selectionArray);  // Adicione esta linha

    const key = `${type}_${chartId}`;
    const interactive = this.state[key].map((each, idx) => {
      return {
        ...each,
        selected: selectionArray[idx]
      };
    });

    // Função para permitir reseleção de elementos
    const reselectElement = (elementType) => {
      const reselectKey = `${elementType}_${chartId}`;
      if (this.state[reselectKey]) {
        const reselected = this.state[reselectKey].map(item => {
          if (item.selected) {
            return { ...item, selected: false };
          }
          return item;
        });
        this.setState({ [reselectKey]: reselected });
      }
    };

    // Lógica específica para cada tipo de elemento
    if (type === 'Trendline') {
      // Desselecionar todos os outros elementos que não sejam Trendline
      const otherElements = ['Fibonacci', 'Alerta']; // Adicione outros tipos de elementos aqui, se houver
      otherElements.forEach(otherType => {
        const otherKey = `${otherType}_${chartId}`;
        if (this.state[otherKey]) {
          const deselected = this.state[otherKey].map(item => ({ ...item, selected: true }));
          this.setState({ [otherKey]: deselected });
        }
      });
    } else if (type === 'Fibonacci') {
      // Desselecionar todos os outros elementos que não sejam Fibonacci
      const otherElements = ['Trendline', 'Alerta']; // Adicione outros tipos de elementos aqui, se houver
      otherElements.forEach(otherType => {
        const otherKey = `${otherType}_${chartId}`;
        if (this.state[otherKey]) {
          const deselected = this.state[otherKey].map(item => ({ ...item, selected: false }));
          this.setState({ [otherKey]: deselected });
        }
      });
    } else if (type === 'Alerta') {
      // Desselecionar todos os outros elementos que não sejam Alerta
      const otherElements = ['Trendline', 'Fibonacci']; // Adicione outros tipos de elementos aqui, se houver
      otherElements.forEach(otherType => {
        const otherKey = `${otherType}_${chartId}`;
        if (this.state[otherKey]) {
          const deselected = this.state[otherKey].map(item => ({ ...item, selected: false }));
          this.setState({ [otherKey]: deselected });
        }
      });
    }

    this.setState({
      [key]: interactive
    }, () => {
      console.log("State after update:", this.state);  // Adicione esta linha
    });
  };
}


export function saveInteractiveNodes(type, chartId) {
	return node => {
		if (isNotDefined(this.interactiveNodes)) {
			this.interactiveNodes = {};
		}
		const key = `${type}_${chartId}`;
		if (isDefined(node) || isDefined(this.interactiveNodes[key])) {
			// console.error(node, key)
			// console.log(this.interactiveNodes)
			// eslint-disable-next-line fp/no-mutation
			this.interactiveNodes = {
				...this.interactiveNodes,
				[key]: { type, chartId, node },
			};
		}
	};
}

export function getInteractiveNodes() {
	return this.interactiveNodes;
}