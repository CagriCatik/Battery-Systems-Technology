import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Fundamentals of Battery Technology',
    description: (
      <>
        Learn the basics of battery chemistry, structure, and functionality to understand their role in modern energy systems.
      </>
    ),
  },
  {
    title: 'Aging and Degradation',
    description: (
      <>
        Explore the factors affecting battery aging and degradation and strategies to mitigate performance losses.
      </>
    ),
  },
  {
    title: 'Chemistry and Design Principles',
    description: (
      <>
        Understand various battery chemistries and principles of designing efficient battery systems.
      </>
    ),
  },
  {
    title: 'Battery Pack Engineering',
    description: (
      <>
        Dive into the design and integration of battery packs for various applications, ensuring safety and reliability.
      </>
    ),
  },
  {
    title: 'Thermal Management',
    description: (
      <>
        Learn techniques for managing heat generation and dissipation to maintain battery efficiency and safety.
      </>
    ),
  },
  {
    title: 'Characteristics and Technical Specifications',
    description: (
      <>
        Understand key technical specifications such as energy density, power density, and cycle life.
      </>
    ),
  },
  {
    title: 'Sizing and Optimization',
    description: (
      <>
        Optimize battery size and capacity to meet specific application requirements and performance goals.
      </>
    ),
  },
  {
    title: 'Battery Management System',
    description: (
      <>
        Learn about BMS features, including monitoring, balancing, and safety mechanisms for batteries.
      </>
    ),
  },
  {
    title: 'BMS Design and Architecture',
    description: (
      <>
        Explore the architecture and design considerations for developing a robust battery management system.
      </>
    ),
  },
  {
    title: 'Modeling and Testing',
    description: (
      <>
        Study methods for battery modeling and testing to predict performance and ensure quality control.
      </>
    ),
  },
];

function Feature({ title, description }) {
  return (
    <div className={clsx(styles.featureBox)}>
      <div className={styles.featureContent}>
        <Heading as="h3" className={styles.featureTitle}>
          {title}
        </Heading>
        <p className={styles.featureDescription}>{description}</p>
      </div>
    </div>
  );
}

export default function BmsFeatures() {
  return (
    <section className={styles.features}>
      {FeatureList.map((props, idx) => (
        <Feature key={idx} {...props} />
      ))}
    </section>
  );
}
